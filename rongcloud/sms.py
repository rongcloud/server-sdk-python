#!/usr/bin/env python
# encoding: utf-8
from .base import RongCloudBase, Response


class SMS(RongCloudBase):
    """Server 开发指南, 请参阅 http://www.rongcloud.cn/docs/server.html"""

    def getImageCode(self, appKey):
        """
        获取图片验证码方法 方法
        @param  appKey:应用Id
	 
        @return code:返回码，200 为正常。
        @return url:返回的图片验证码 URL 地址。
        @return verifyId:返回图片验证标识 Id。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "SMSImageCodeReslut",
            "desc": " getImageCode 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "url",
                "type": "String",
                "desc": "返回的图片验证码 URL 地址。"
            }, {
                "name": "verifyId",
                "type": "String",
                "desc": "返回图片验证标识 Id。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('SMS', 'GET', ''),
            action='/getImgCode.json',
            params={"appKey": appKey})
        return Response(r, desc)

    def sendCode(self,
                 mobile,
                 templateId,
                 region,
                 verifyId=None,
                 verifyCode=None):
        """
        发送短信验证码方法。 方法
        @param  mobile:接收短信验证码的目标手机号，每分钟同一手机号只能发送一次短信验证码，同一手机号 1 小时内最多发送 3 次。（必传）
        @param  templateId:短信模板 Id，在开发者后台->短信服务->服务设置->短信模版中获取。（必传）
        @param  region:手机号码所属国家区号，目前只支持中图区号 86）
        @param  verifyId:图片验证标识 Id ，开启图片验证功能后此参数必传，否则可以不传。在获取图片验证码方法返回值中获取。
        @param  verifyCode:图片验证码，开启图片验证功能后此参数必传，否则可以不传。
	 
        @return code:返回码，200 为正常。
        @return sessionId:短信验证码唯一标识。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "SMSSendCodeReslut",
            "desc": " SMSSendCodeReslut 成功返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "sessionId",
                "type": "String",
                "desc": "短信验证码唯一标识。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('SMS', 'POST', 'application/x-www-form-urlencoded'),
            action='/sendCode.json',
            params={
                "mobile": mobile,
                "templateId": templateId,
                "region": region,
                "verifyId": verifyId,
                "verifyCode": verifyCode
            })
        return Response(r, desc)

    def verifyCode(self, sessionId, code):
        """
        验证码验证方法 方法
        @param  sessionId:短信验证码唯一标识，在发送短信验证码方法，返回值中获取。（必传）
        @param  code:短信验证码内容。（必传）
	 
        @return code:返回码，200 为正常。
        @return success:true 验证成功，false 验证失败。
        @return errorMessage:错误信息。
	    """

        desc = {
            "name": "SMSVerifyCodeResult",
            "desc": " VerifyCode 返回结果",
            "fields": [{
                "name": "code",
                "type": "Integer",
                "desc": "返回码，200 为正常。"
            }, {
                "name": "success",
                "type": "Boolean",
                "desc": "true 验证成功，false 验证失败。"
            }, {
                "name": "errorMessage",
                "type": "String",
                "desc": "错误信息。"
            }]
        }
        r = self.call_api(
            method=('SMS', 'POST', 'application/x-www-form-urlencoded'),
            action='/verifyCode.json',
            params={"sessionId": sessionId,
                    "code": code})
        return Response(r, desc)
