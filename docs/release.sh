#!/bin/bash
# @filename    :  release.sh
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-03-29T16:11:22+08:00
# @require     :  GNU bash, version 5.2.15(1)
# @function    :

source /home/android/bin/module/prelude.sh
source /home/android/bin/module/gio.sh
source /home/android/bin/module/utils.sh

readonly MFS_SERVER="/run/user/1000/gvfs/smb-share:server=10.231.13.5,share=share/SW/System"
readonly MFS_CAMERA_DIR="${MFS_SERVER}/0-Member/church.zhong/camera/"
PROJECT_ROOT=$(dirname "${WORK_DIR}")
echo "# PROJECT_ROOT = ${PROJECT_ROOT}"
OS_DATE_DAY=$(date +%Y_%m_%d)
echo "# OS_DATE_DAY  = ${OS_DATE_DAY}"

# -------------------------------- usage --------------------------------
function usage() { echo "Usage: $0 [-c <clean>] [-f <format>] [-r <release>]" 1>&2; }
CLEAN=false
FORMAT=false
RELEASE=false
while getopts ":cfr" o; do
	case "${o}" in
	c)
		CLEAN=true
		;;
	f)
		FORMAT=true
		;;
	r)
		RELEASE=true
		;;
	*)
		usage
		exit "${EX_USAGE}"
		;;
	esac
done
shift $((OPTIND - 1))
RELEASE=false
echo "# CLEAN        = ${CLEAN}"
echo "# FORMAT       = ${FORMAT}"
# -------------------------------- usage --------------------------------

function clean() {
	echo "# clean project"
	PROJECT_DIRS=(
		"${PROJECT_ROOT}/pymannkendall"
		"${PROJECT_ROOT}/docs"
		"${PROJECT_ROOT}/trends"
		"${PROJECT_ROOT}/utils"
	)

	for dir in "${PROJECT_DIRS[@]}"; do
		if [[ ! -d "${dir}" ]]; then
			enoent "${dir}"
			continue
		fi

		find "${dir}" -type d \( -name ".pytest_cache" -o -name "__pycache__" -o -name ".mypy_cache" -o -name ".ruff_cache" -o -name "target" \) | while read -r line; do
			rm -rf "${line}"
		done
	done
	find "${PROJECT_ROOT}" -type d \( -name ".pytest_cache" -o -name "__pycache__" -o -name ".mypy_cache" -o -name ".ruff_cache" -o -name "target" \) | while read -r line; do
		rm -rf "${line}"
	done

	find "${PROJECT_ROOT}/docs" -type f -name "Cargo.toml" | sort | while read -r file; do
		echo "clean ${file}"
		cargo clean --quiet --manifest-path "${file}"
	done
}

function format() {
	echo "# format project"
	PROJECT_DIRS=(
		"${PROJECT_ROOT}/docs"
		"${PROJECT_ROOT}/trends"
		"${PROJECT_ROOT}/utils"
	)

	for dir in "${PROJECT_DIRS[@]}"; do
		if [[ ! -d "${dir}" ]]; then
			enoent "${dir}"
			continue
		fi

		find "${dir}" -type f \( -name "*.py" -o -name "*.sh" \) | while read -r file; do
			fmt.py -r -f "${file}"
		done
	done

	find "${PROJECT_ROOT}" -maxdepth 1 -type f | while read -r file; do
		if [[ "${file}" == *"xmltodict.py" ]]; then
			continue
		fi
		fmt.py -r -f "${file}"
	done
}

function upload() {
	LOCAL_CAMERA_ROOT=$(dirname "${PROJECT_ROOT}")
	PROJECT_BASENAME=$(basename "${PROJECT_ROOT}")

	tgz_basename="${PROJECT_BASENAME}_${OS_DATE_DAY}.tgz"
	tgz_filename="${LOCAL_CAMERA_ROOT}/${tgz_basename}"

	################################################################
	tar -czf "${tgz_filename}" -C "${LOCAL_CAMERA_ROOT}" "${PROJECT_BASENAME}"
	################################################################

	################################################################
	cp -f "${tgz_filename}" "${MFS_CAMERA_DIR}/${tgz_basename}"
	echo "${tgz_filename}"
	echo "${MFS_CAMERA_DIR}/${tgz_basename}"
	################################################################
}

function release() {
	################################################################
	clean
	################################################################

	################################################################
	# format
	################################################################

	################################################################
	mount_share
	################################################################

	################################################################
	upload
	################################################################
}

function main() {
	if [[ "true" = "${CLEAN}" ]]; then
		clean
	fi

	if [[ "true" = "${FORMAT}" ]]; then
		format
	fi

	if [[ "true" = "${RELEASE}" ]]; then
		release
	fi
}

source /home/android/bin/module/postlude.sh
