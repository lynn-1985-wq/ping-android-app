[app]
title = IP Ping检测工具
package.name = pingcheck
package.domain = org.netping

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
android.accept_sdk_license = True