USE_CAMERA_STUB := false

# Dalvik
TARGET_ARCH_LOWMEM := true

# inherit from the proprietary version
-include vendor/htc/z4u/BoardConfigVendor.mk

TARGET_ARCH := arm
TARGET_NO_BOOTLOADER := true
TARGET_BOARD_PLATFORM_GPU := qcom-adreno203
TARGET_BOARD_PLATFORM := msm8225q
TARGET_CPU_ABI := armeabi-v7a
TARGET_CPU_ABI2 := armeabi
TARGET_ARCH_VARIANT := armv7-a-neon
TARGET_CPU_VARIANT := cortex-a5
ARCH_ARM_HAVE_TLS_REGISTER := true
#BOARD_EGL_CFG := device/htc/z4u/egl.cfg

TARGET_BOOTLOADER_BOARD_NAME := z4u

BOARD_KERNEL_CMDLINE := no_console_suspend=1 console=/dev/tty0 msm_fb.align_buffer=N ats=1l
BOARD_KERNEL_BASE := 0x03b00000
BOARD_KERNEL_PAGESIZE := 2048

TARGET_USERIMAGES_USE_EXT4 := true

# fix this up by examining /proc/mtd on a running device
BOARD_BOOTIMAGE_PARTITION_SIZE :=     16776192
BOARD_RECOVERYIMAGE_PARTITION_SIZE := 16776704
BOARD_SYSTEMIMAGE_PARTITION_SIZE :=   2013264896
BOARD_USERDATAIMAGE_PARTITION_SIZE := 1342177280
BOARD_FLASH_BLOCK_SIZE := 131072

TARGET_PREBUILT_KERNEL := device/htc/z4u/kernel

BOARD_HAS_NO_SELECT_BUTTON := true

# Flags
COMMON_GLOBAL_CFLAGS += -DHTCLOG
