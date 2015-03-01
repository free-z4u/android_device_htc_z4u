$(call inherit-product, $(SRC_TARGET_DIR)/product/languages_full.mk)

# The gps config appropriate for this device
$(call inherit-product, device/common/gps/gps_us_supl.mk)

$(call inherit-product-if-exists, vendor/htc/z4u/z4u-vendor.mk)

DEVICE_PACKAGE_OVERLAYS += device/htc/z4u/overlay

TARGET_KERNEL_SOURCE := kernel/htc/z4u
TARGET_KERNEL_CONFIG := z4u_with_wifi_defconfig
TARGET_KERNEL_RECOVERY_CONFIG := z4u_with_wifi_defconfig

$(call inherit-product, build/target/product/full.mk)

PRODUCT_BUILD_PROP_OVERRIDES += BUILD_UTC_DATE=0
PRODUCT_NAME := full_z4u
PRODUCT_DEVICE := z4u

# Init files
PRODUCT_COPY_FILES += \
    $(LOCAL_PATH)/fstab.z4u:root/fstab.z4u \
    $(LOCAL_PATH)/ueventd.z4u.rc:root/ueventd.z4u.rc \
    $(LOCAL_PATH)/init.z4u.rc:root/init.z4u.rc \
    $(LOCAL_PATH)/msmlogo.rle:root/msmlogo.rle \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/athwlan.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/athwlan.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.SD31.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.SD31.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.SD32.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.SD32.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.WB31.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/bdata.WB31.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/data.patch.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/data.patch.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/endpointping.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/endpointping.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/fw-2.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/fw-2.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/fw-3.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/fw-3.bin \
    $(LOCAL_PATH)/system/etc/firmware/ath6k/AR6003/hw2.1.1/otp.bin:system/etc/firmware/ath6k/AR6003/hw2.1.1/otp.bin

