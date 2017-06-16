;/*!component/const/user.js*/
define("component/const/user",function(e,n){"use strict";Object.defineProperty(n,"__esModule",{value:!0});n.USER_AGE={1:"小学",2:"中学",3:"大学",4:"其他"},n.USER_LEVEL={1:"核心",2:"活跃",3:"小白",4:"其他"},n.USER_OPERATOR={0:"无",1:"王佳",2:"刘瑞芳",3:"蒋志鹏",4:"曹雪静",5:"王实龙",6:"罗红云"}});
;/*!component/api/index.js*/
define("component/api/index",function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var n=(e("component/const/user"),"/aweme/op/api");t.default={SEARCH_USERS:n+"/user/search/",GET_SEARCH_LIST:n+"/item/items/"}});
;/*!component/util/index.js*/
define("component/util/index",function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});t.test=function(){console.log("test")},t.test2=function(){console.log("test2")}});
;/*!component/common/footer/index.js*/
define("component/common/footer/index",function(e,o){"use strict";Object.defineProperty(o,"__esModule",{value:!0}),o.init=void 0;{var n=e("component/util/index");o.init=function(e){console.log("footer: "+e),n.test2()}}});
;/*!component/common/header/index.js*/
define("component/common/header/index",function(e,n){"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.init=void 0;{var o=e("component/util/index");n.init=function(e){console.log("header: "+e.username),o.test()}}});
;/*!component/util/url.js*/
define("component/util/url",function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0}),t.default={getQueryStr:function(){console.log(location.href)}}});