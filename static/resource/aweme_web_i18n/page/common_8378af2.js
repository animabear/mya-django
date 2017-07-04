;/*!web_i18n:component/const/user.js*/
define("web_i18n:component/const/user",function(e,n){Object.defineProperty(n,"__esModule",{value:!0});n.USER_AGE={1:"小学",2:"中学",3:"大学",4:"其他"},n.USER_LEVEL={1:"核心",2:"活跃",3:"小白",4:"其他"},n.USER_OPERATOR={0:"无",1:"王佳",2:"刘瑞芳",3:"蒋志鹏",4:"曹雪静",5:"王实龙",6:"罗红云"}});
;/*!web_i18n:component/api/index.js*/
define("web_i18n:component/api/index",function(e,n){Object.defineProperty(n,"__esModule",{value:!0});var i=(e("web_i18n:component/const/user"),"/aweme/op/api");n.default={SEARCH_USERS:i+"/user/search/",GET_SEARCH_LIST:i+"/item/items/"}});
;/*!web_i18n:component/util/index.js*/
define("web_i18n:component/util/index",function(e,t){Object.defineProperty(t,"__esModule",{value:!0});t.test=function(){console.log("test")},t.test2=function(){console.log("test2")}});
;/*!web_i18n:component/common/footer/index.js*/
define("web_i18n:component/common/footer/index",function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.init=void 0;{var o=e("web_i18n:component/util/index");n.init=function(e){console.log("footer: "+e),o.test2()}}});
;/*!web_i18n:component/common/header/index.js*/
define("web_i18n:component/common/header/index",function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.init=void 0;{var i=e("web_i18n:component/util/index");n.init=function(e){console.log("header: "+e.username),i.test()}}});
;/*!web_i18n:component/util/url.js*/
define("web_i18n:component/util/url",function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.default={getQueryStr:function(){console.log(location.href)}}});