;/*!web:component/const/user.js*/
define("web:component/const/user",function(e,n){Object.defineProperty(n,"__esModule",{value:!0});n.USER_AGE={1:"小学",2:"中学",3:"大学",4:"其他"},n.USER_LEVEL={1:"核心",2:"活跃",3:"小白",4:"其他"},n.USER_OPERATOR={0:"无",1:"王佳",2:"刘瑞芳",3:"蒋志鹏",4:"曹雪静",5:"王实龙",6:"罗红云"}});
;/*!web:component/api/index.js*/
define("web:component/api/index",function(e,n){Object.defineProperty(n,"__esModule",{value:!0});var o=(e("web:component/const/user"),"/aweme/op/api");n.default={SEARCH_USERS:o+"/user/search/",GET_SEARCH_LIST:o+"/item/items/"}});
;/*!web:component/util/index.js*/
define("web:component/util/index",function(e,t){Object.defineProperty(t,"__esModule",{value:!0});t.test=function(){console.log("test")},t.test2=function(){console.log("test2")}});
;/*!web:component/common/footer/index.js*/
define("web:component/common/footer/index",function(e,o){Object.defineProperty(o,"__esModule",{value:!0}),o.init=void 0;{var n=e("web:component/util/index");o.init=function(e){console.log("footer: "+e),n.test2()}}});
;/*!web:component/common/header/index.js*/
define("web:component/common/header/index",function(e,n){Object.defineProperty(n,"__esModule",{value:!0}),n.init=void 0;{var o=e("web:component/util/index");n.init=function(e){console.log("header: "+e.username),o.test()}}});
;/*!web:component/util/url.js*/
define("web:component/util/url",function(e,o){Object.defineProperty(o,"__esModule",{value:!0}),o.default={getQueryStr:function(){console.log(location.href)}}});