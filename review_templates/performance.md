# Performance Code Review Template

## Algorithm Efficiency
- [ ] Time complexity is appropriate for expected data size
- [ ] Space complexity is optimized
- [ ] Algorithms chosen are appropriate for the use case
- [ ] No redundant computations or inefficient loops

## Resource Management
- [ ] Memory usage is optimized
- [ ] Resources are properly released/disposed
- [ ] Connection pooling is used where appropriate
- [ ] No memory leaks identified

## Data Access & Storage
- [ ] Database queries are optimized
- [ ] Appropriate indexes are used
- [ ] Batch operations used where applicable
- [ ] Data caching strategy is implemented where appropriate

## Concurrency & Parallelism
- [ ] Thread-safety concerns are addressed
- [ ] Parallelization opportunities are utilized
- [ ] Deadlock and race condition risks are mitigated
- [ ] Asynchronous operations are properly implemented

## General Optimizations
- [ ] Code avoids premature optimization
- [ ] Hot paths are identified and optimized
- [ ] Appropriate caching strategies are used
- [ ] Performance metrics/monitoring is implemented

## Additional Notes:
(Add any specific performance observations or suggestions here)