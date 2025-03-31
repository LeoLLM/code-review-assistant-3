# Performance Code Review Template

## Review Metadata
- **Reviewer:** [Name]
- **Date:** [YYYY-MM-DD]
- **Component/Module:** [Name]
- **Language/Framework:** [Language]
- **Performance Critical:** [Yes/No]

## Complexity Metrics
- [ ] Cyclomatic complexity is within acceptable limits (<10 per function)
- [ ] Cognitive complexity is maintained at readable levels
- [ ] Depth of inheritance is appropriate (<5 levels)
- [ ] Method/Function length is appropriate (<100 lines)
- [ ] Class/Module size is appropriate (<500 lines)

## Algorithm Efficiency
- [ ] Time complexity is appropriate for expected data size (specify: O(X))
- [ ] Space complexity is optimized (specify: O(X))
- [ ] Algorithms chosen are appropriate for the use case
- [ ] No redundant computations or inefficient loops
- [ ] Data structures are optimal for operations performed

## Memory Management
- [ ] Memory usage is profiled and optimized
- [ ] Resources are properly released/disposed
- [ ] Memory leaks addressed (profiler results attached if applicable)
- [ ] Object pooling used where appropriate
- [ ] Memory allocation patterns are optimized (reduced garbage collection)

## Data Access & Storage
- [ ] Database queries are optimized (explain plans checked)
- [ ] Appropriate indexes are used
- [ ] Batch operations used where applicable
- [ ] Data caching strategy is implemented where appropriate
- [ ] N+1 query problems are eliminated

## Concurrency & Parallelism
- [ ] Thread-safety concerns are addressed
- [ ] Parallelization opportunities are utilized
- [ ] Deadlock and race condition risks are mitigated
- [ ] Asynchronous operations are properly implemented
- [ ] Thread pool/async configuration is optimized

## I/O Operations
- [ ] I/O operations are minimized
- [ ] Buffering is used appropriately
- [ ] Non-blocking I/O is used where applicable
- [ ] File operations are optimized
- [ ] Network calls are minimized and optimized

## Runtime Performance
- [ ] Hot paths are identified and optimized
- [ ] Start-up time is acceptable
- [ ] Response time meets requirements (specify target: Xms)
- [ ] Throughput meets requirements (specify target: X req/sec)
- [ ] Resource utilization is monitored and controlled

## Optimization Techniques
- [ ] Code avoids premature optimization
- [ ] Appropriate caching strategies are used
- [ ] Lazy loading implemented where beneficial
- [ ] Compiled/optimized code paths for critical sections
- [ ] Performance metrics/monitoring is implemented

## Performance Testing Evidence
- [ ] Load testing results are acceptable (attach results)
- [ ] Stress testing has been performed
- [ ] Memory profiling has been conducted
- [ ] CPU profiling has been conducted
- [ ] Performance regression tests are in place

## Specific Performance Findings

### Finding 1: [Brief description]
- **Location:** [file:line]
- **Current Performance:** [metric]
- **Target Performance:** [metric]
- **Impact:** [Low/Medium/High]
- **Recommendation:** [Specific action to improve]

### Finding 2: [Brief description]
- **Location:** [file:line]
- **Current Performance:** [metric]
- **Target Performance:** [metric]
- **Impact:** [Low/Medium/High]
- **Recommendation:** [Specific action to improve]

## Resources
- [Language-specific performance best practices]
- [Framework-specific optimization guidelines]
- [Profiling tools reference]
- [Benchmarking methodology]