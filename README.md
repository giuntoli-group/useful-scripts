## Build a Slurm pipeline

Split a long simulation into smaller parts and run them one after the other in Slurm.

```bash
#!/bin/bash

# submit the first job without any dependency
id=$( sbatch submit.sh)

# submit 10 successive jobs each starting after the previous one ends/timeouts.
for i in {1..10}
do
  id=$( sbatch --dependency=afterany:${id##* } submit.sh )
done
```
