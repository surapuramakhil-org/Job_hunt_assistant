"use strict";
$(function () {
    var POST_PATH = '/parseResume';
    var MAX_FILE_SIZE = 100 * 1000 * 1000;
    var req;
    var userTouchedInputs = new Map();
    var accountId = $('input[name=accountId]').val();
    var failure = $('.resume-upload-failure');
    var success = $('.resume-upload-success');
    var working = $('.resume-upload-working');
    var oversizeFailure = $('.resume-upload-oversize');
    var parsedInputFields = [
        $('input[name=org]'),
        $('input[name=phone]'),
        $('input[name=name]'),
        $('input[name=email]'),
        $('input[name=location]'),
        $('input[name="urls[LinkedIn]"]'),
        $('input[name="urls[Twitter]"]'),
        $('input[name="urls[Quora]"]'),
        $('input[name="urls[GitHub]"]'),
        $('input[name="urls[Other]"]'),
    ];
    function parseData(data) {
        var profileData;
        try {
            profileData = JSON.parse(data);
        }
        catch (e) {
            return;
        }
        if (!profileData) {
            return;
        }
        return profileData;
    }
    function updateFields(profileData) {
        var _a;
        if (!profileData) {
            failure.show();
            return;
        }
        success.show();
        updateIfUntouched($('input[name=org]'), profileData === null || profileData === void 0 ? void 0 : profileData.position);
        updateIfUntouched($('input[name=phone]'), profileData === null || profileData === void 0 ? void 0 : profileData.phone);
        updateIfUntouched($('input[name=name]'), profileData === null || profileData === void 0 ? void 0 : profileData.name);
        updateIfUntouched($('input[name=email]'), profileData === null || profileData === void 0 ? void 0 : profileData.email);
        updateIfUntouched($('input[name=location]'), (_a = profileData === null || profileData === void 0 ? void 0 : profileData.location) === null || _a === void 0 ? void 0 : _a.name);
        updateIfUntouched($('input[name=selectedLocation]'), JSON.stringify(profileData === null || profileData === void 0 ? void 0 : profileData.location));
        var links = (profileData === null || profileData === void 0 ? void 0 : profileData.links) || [];
        var urlNames = ['LinkedIn', 'Twitter', 'Quora', 'GitHub', 'Other'];
        var urlNamesWithoutLast = urlNames.slice(0, -1);
        var foundUrls = new Map();
        var _loop_1 = function (link) {
            var name_1 = urlNamesWithoutLast.find(function (name) { return link.domain && link.domain.toLowerCase().indexOf(name.toLowerCase()) > -1; });
            foundUrls.set(name_1 || 'Other', link.url);
        };
        for (var _i = 0, links_1 = links; _i < links_1.length; _i++) {
            var link = links_1[_i];
            _loop_1(link);
        }
        for (var _b = 0, urlNames_1 = urlNames; _b < urlNames_1.length; _b++) {
            var field = urlNames_1[_b];
            updateIfUntouched($('input[name="urls[' + field + ']"]'), foundUrls.get(field));
        }
        if (profileData.resumeStorageId) {
            updateIfUntouched($('input[name=resumeStorageId]'), profileData.resumeStorageId);
        }
    }
    function updateIfUntouched(field, value) {
        var formFieldExists = field && getFirstElement(field);
        var userTouchedThis = userTouchedInputs.get(getFirstElement(field)) && field.val();
        if (!formFieldExists) {
            return;
        }
        else if (!userTouchedThis) {
            userTouchedInputs.set(getFirstElement(field), false);
            field.val(value || '');
        }
    }
    function getFirstElement(field) {
        return field === null || field === void 0 ? void 0 : field.get(0);
    }
    function addInputChangeListener(field) {
        field.on('change paste', function () {
            userTouchedInputs.set(getFirstElement(field), true);
        });
    }
    $(function () {
        parsedInputFields.forEach(function (field) {
            if (field && getFirstElement(field))
                addInputChangeListener(field);
        });
    });
    $('#resume-upload-input').on('change', function () {
        var _a;
        failure.hide();
        success.hide();
        working.hide();
        oversizeFailure.hide();
        var file = (_a = this === null || this === void 0 ? void 0 : this.files) === null || _a === void 0 ? void 0 : _a[0];
        if (!file || file.size === 0) {
            return;
        }
        if (file.size > MAX_FILE_SIZE) {
            oversizeFailure.show();
            return;
        }
        working.show();
        var formData = new FormData();
        formData.append('resume', file);
        formData.append('accountId', accountId);
        if (req && req.readyState < 4) {
            req.abort();
        }
        req = new XMLHttpRequest();
        req.onreadystatechange = function () {
            if (req.readyState === 4) {
                working.hide();
                if (req.status === 200) {
                    var profile = parseData(req.response);
                    updateFields(profile);
                }
                else if (req.status === 400 && req.responseText === 'PayloadTooLargeError') {
                    oversizeFailure.show();
                }
                else {
                    failure.show();
                }
            }
        };
        req.open('POST', POST_PATH, true);
        req.send(formData);
    });
});
//# sourceMappingURL=parseResume.js.map