#!/bin/bash
trap "exit" INT

OFFSET=1
ITER=10000
LOOP=1
PARALLEL=8

start=$(date +"%s")

rm output.txt

for runtime in 27 35; do (
    for name in sortedlist sorteddict sortedset; do (
        for j in $(seq 1 $LOOP); do (
            for i in $(seq 1 $PARALLEL); do (
                echo ". env$runtime/bin/activate && python -m tests.test_stress_$name $ITER $OFFSET$runtime$j$i >> output.txt 2>&1" | tee -a output.txt | bash
            ) & done
            wait
        ) done
    ) done
) done

cat output.txt

end=$(date +"%s")
diff=$(($end - $start))
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
diff=$(($diff * $PARALLEL))
echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds of stress."
