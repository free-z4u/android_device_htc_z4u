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
PRODUCT_PACKAGES += \
    fstab.qcom \
    init.target.rc \
    remount.qcom

# Recovery
PRODUCT_COPY_FILES += \
    device/htc/z4u/rootdir/etc/fstab.qcom:recovery/root/fstab.qcom

PRODUCT_BUILD_PROP_OVERRIDES += BUILD_UTC_DATE=0
PRODUCT_NAME := full_z4u
PRODUCT_DEVICE := z4u
