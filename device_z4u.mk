$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)

# The gps config appropriate for this device
$(call inherit-product, device/common/gps/gps_us_supl.mk)

$(call inherit-product-if-exists, vendor/htc/z4u/z4u-vendor.mk)

DEVICE_PACKAGE_OVERLAYS += device/htc/z4u/overlay

TARGET_KERNEL_SOURCE := kernel/htc/z4u
TARGET_KERNEL_CONFIG := z4u_defconfig
TARGET_KERNEL_RECOVERY_CONFIG := z4u_defconfig

$(call inherit-product, build/target/product/full.mk)

# vold config
PRODUCT_COPY_FILES += \
    device/htc/z4u/configs/vold.fstab:system/etc/vold.fstab

# Boot ramdisk setup
PRODUCT_COPY_FILES += \
    device/htc/z4u/rootdir/bt_permission.sh:root/bt_permission.sh \
    device/htc/z4u/rootdir/cwkeys:root/cwkeys \
    device/htc/z4u/rootdir/fstab.z4u:root/fstab.z4u \
    device/htc/z4u/rootdir/init.qcom.rc:root/init.qcom.rc \
    device/htc/z4u/rootdir/init.qcom.sh:root/init.qcom.sh \
    device/htc/z4u/rootdir/init.target.rc:root/init.target.rc \
    device/htc/z4u/rootdir/init.target.recovery.rc:root/init.target.recovery.rc \
    device/htc/z4u/rootdir/remount.qcom:root/remount.qcom \
    device/htc/z4u/rootdir/sbin/gzip_recvy:root/sbin/gzip_recvy \
    device/htc/z4u/rootdir/sbin/htc_ebdlogd_recvy:root/sbin/htc_ebdlogd_recvy \
    device/htc/z4u/rootdir/sbin/logcat2_recvy:root/sbin/logcat2_recvy \
    device/htc/z4u/rootdir/sbin/sfc:root/sbin/sfc \
    device/htc/z4u/rootdir/ueventd.target.rc:root/ueventd.target.rc

# Recovery
PRODUCT_COPY_FILES += \
    device/htc/z4u/rootdir/fstab.z4u:recovery/root/fstab.z4u

PRODUCT_BUILD_PROP_OVERRIDES += BUILD_UTC_DATE=0
PRODUCT_NAME := full_z4u
PRODUCT_DEVICE := z4u
