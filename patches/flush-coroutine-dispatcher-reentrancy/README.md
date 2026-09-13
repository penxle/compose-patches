# FlushCoroutineDispatcher reentrancy

Make synchronous task flushing safe when a running task calls `flush()` again. This dispatcher is shared by iOS and Compose Desktop;
Android uses a separate dispatcher that already removes pending tasks before running them.

The old implementation swapped two task queues before iterating a batch. A nested flush could swap the active batch back into the pending
queue and execute a completed coroutine again. Native text-input callbacks can trigger this by synchronously requesting a frame while an
outer frame is still dispatching work.

- Remove each task from the pending queue before invoking it, so nested flushes see only work that has not started. Remaining tasks retain
  their queue order, including tasks enqueued by callbacks.
- Restore the previous running state after each dispatch, so returning from a nested flush does not report the outer task as idle.
- Keep the existing execution lock and delayed-task cancellation behavior. The spare queue is no longer needed.

This fixes dispatcher queue ownership independently of the native edit-generation handling in `ios-text-input-composition-sync`.

The two new shared tests cover reentrant execution order, exactly-once execution, and running-state preservation. Both fail on the original
implementation. With the existing 1.12.0 release patches applied, focused verification passes: 10 desktop dispatcher tests, 8 iOS dispatcher
tests, 31 iOS text-input tests, and iOS arm64 compilation. Existing desktop coverage includes flushing from another thread.
