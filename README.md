# 
用python完成的一些爬虫小项目


########## 在线有道翻译接口加密方式破解####################
在POST表单中   fanyi.min.js文件对 salt sign两个参数进行加密
原代码如下：
'''
t.asyRequest = function(e) {
        var t = e.i
          , i = "" + ((new Date).getTime() + parseInt(10 * Math.random(), 10))
          , o = n.md5("fanyideskweb" + t + i + "ebSeFb%=XZ%T[KZ)c(sy!");
        r && r.abort(),
        r = n.ajax({
            type: "POST",
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            url: "/bbk/translate_m.do",
            data: {
                i: e.i,
                client: "fanyideskweb",
                salt: i,
                sign: o,
                tgt: e.tgt,
                from: e.from,
                to: e.to,
                doctype: "json",
                version: "3.0",
                cache: !0
            },
            dataType: "json",
            success: function(t) {
                t && 0 == t.errorCode ? e.success && e.success(t) : e.error && e.error(t)
            },
            error: function(e) {}
        })
'''
salt 参数为一个时间戳（以毫秒为单位，因为是13位数字）再加一个0-10之间的随机整数
sign 参数中 t 是要翻译的内容
