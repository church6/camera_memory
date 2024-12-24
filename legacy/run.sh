#!/bin/bash
# shellcheck disable=SC2317
# @filename    :  run.sh
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-03-27T17:37:45+08:00
source /home/android/bin/module/prelude.sh
source /home/android/bin/module/utils.sh
source /home/android/bin/module/time.sh

function work() {
	find "/data/ro/camera_test_logs" -maxdepth 1 -type d -name "pytest_*" | sort | while read -r log; do
		# echo "${log}"
		python3 "${WORK_DIR}/analyze.py" -p "${log}"
	done
}

function appinfo_2() {
	find "/data/ro/camera_test_logs" -maxdepth 4 -type f -name "appinfo_2.csv" | while read -r file; do
		echo "----------------------------------------------------------------"
		echo "${file}"
		enter=$(sed '2q;d' "${file}")
		echo "${enter}"
		enter_pid=$(echo "${enter}" | awk -F',' '{print $2}')
		leave=$(tail -n 1 "${file}")
		echo "${leave}"
		leave_pid=$(echo "${leave}" | awk -F',' '{print $2}')
		if [[ "${enter_pid}" -ne "${leave_pid}" ]]; then
			echo -e "\033[31m provider crash \033[0m"
		fi
		echo "----------------------------------------------------------------"
	done | tee "/data/ro/output/camera_provider_${OS_DATE_SECOND}.log"
}

function main() {
	work | tee "/data/ro/output/camera_memory_${OS_DATE_SECOND}.log"
}

source /home/android/bin/module/postlude.sh
