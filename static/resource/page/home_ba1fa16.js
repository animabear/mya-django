;/*!component/home/comp1/index.js*/
define("component/home/comp1/index",function(n,e){"use strict";function o(n){return n&&n.__esModule?n:{"default":n}}{var t=n("component/util/index"),i=n("component/api/index");o(i)}e.init=function(){console.log("comp1"),t.test()}});
;/*!component/home/comp2/index.js*/
define("component/home/comp2/index",function(n,o){"use strict";var e=n("component/util/index");o.init=function(){console.log("comp2"),e.test2()}});
;/*!page/home/index.js*/
define("page/home/index",function(e,t){"use strict";function n(e){return e&&e.__esModule?e:{"default":e}}function o(){console.log("home page"),i.default.getQueryStr()}Object.defineProperty(t,"__esModule",{value:!0}),t.init=o;var u=e("component/util/url"),i=n(u)});