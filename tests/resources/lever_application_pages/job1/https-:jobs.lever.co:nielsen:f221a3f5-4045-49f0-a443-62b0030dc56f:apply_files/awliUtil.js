"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
function linkedInLocationToTextKernel(linkedInLocation) {
    if (!(linkedInLocation === null || linkedInLocation === void 0 ? void 0 : linkedInLocation.locationName) && !(linkedInLocation === null || linkedInLocation === void 0 ? void 0 : linkedInLocation.country))
        return;
    if (!linkedInLocation.locationName) {
        linkedInLocation.locationName = countryCodeToFullName(linkedInLocation.country.toUpperCase());
    }
    var textKernelLocation = __assign(__assign({}, (linkedInLocation.locationName && { name: linkedInLocation.locationName })), (linkedInLocation.country && {
        address: { country: { code: linkedInLocation.country.toUpperCase() } },
    }));
    return textKernelLocation;
}
function countryCodeToFullName(countryCode) {
    var countryName;
    if (countryCode) {
        try {
            var regionNames = new Intl.DisplayNames(['en'], { type: 'region' });
            countryName = regionNames.of(countryCode);
        }
        catch (error) {
            return;
        }
    }
    return countryName;
}
//# sourceMappingURL=awliUtil.js.map