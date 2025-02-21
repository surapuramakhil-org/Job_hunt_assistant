/*!
 *  javascript-debounce 1.0.1
 *
 *  A lightweight, dependency-free JavaScript module for debouncing functions based on David Walsh's debounce function.
 *
 *  Source code available at: https://github.com/jgarber623/javascript-debounce
 *
 *  (c) 2015-2019 Jason Garber (http://sixtwothree.org)
 *
 *  javascript-debounce may be freely distributed under the MIT license.
 */

!function(e,t){"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?module.exports=t():e.debounce=t()}(this,function(){"use strict";return function(e,t){var n;return function(){var o=this,i=arguments;clearTimeout(n),n=setTimeout(function(){e.apply(o,i)},t)}}});
