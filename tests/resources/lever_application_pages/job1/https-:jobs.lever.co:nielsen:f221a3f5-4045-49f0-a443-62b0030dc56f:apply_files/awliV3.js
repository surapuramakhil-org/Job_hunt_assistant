"use strict";
var MESSAGE_ORIGIN = 'https://www.linkedin.com';
var BUTTON_SELECTOR = '.awli-button';
var receivedData = null;
var userHasClicked = false;
var overlayButton = OverlayButton(BUTTON_SELECTOR, function () {
    userHasClicked = true;
    if (receivedData) {
        fillApplicationForm(receivedData);
    }
});
function OverlayButton(selector, onClick) {
    var BUTTON_MASK_CLASS = 'button-masked';
    var BUTTON_STATES = ['loading', 'ready', 'completed'];
    var $button = $(selector);
    var setState = function (state) {
        for (var _i = 0, BUTTON_STATES_1 = BUTTON_STATES; _i < BUTTON_STATES_1.length; _i++) {
            var buttonState = BUTTON_STATES_1[_i];
            var buttonStateClass = "state-".concat(buttonState);
            if (state === buttonState) {
                $button.addClass(buttonStateClass);
            }
            else {
                $button.removeClass(buttonStateClass);
            }
        }
    };
    var showMask = function () {
        $button.addClass(BUTTON_MASK_CLASS);
    };
    var hideMask = function () {
        $button.removeClass(BUTTON_MASK_CLASS);
    };
    $button.on('click', function () {
        setState('loading');
        setTimeout(function () {
            setState('completed');
            if (onClick) {
                onClick();
            }
        }, 300);
    });
    return {
        setState: setState,
        showMask: showMask,
        hideMask: hideMask,
    };
}
function fillApplicationForm(data) {
    var _a, _b;
    var applicationFormData = {
        'name': "".concat(data.firstName, " ").concat(data.lastName).trim(),
        'email': (_a = data.emailAddress) === null || _a === void 0 ? void 0 : _a.toLowerCase(),
        'phone': data.phoneNumber,
        'urls[LinkedIn]': data.publicProfileUrl,
        'linkedInData': JSON.stringify(data),
    };
    if (data.textKernelLocation) {
        applicationFormData.location = data.textKernelLocation.name;
        applicationFormData.selectedLocation = JSON.stringify(data.textKernelLocation);
    }
    if (data.positions) {
        var currentPosition = data.positions.find(function (position) { return position.isCurrent; });
        if (currentPosition) {
            var companyName = currentPosition.companyName || ((_b = currentPosition.company) === null || _b === void 0 ? void 0 : _b.name);
            if (companyName) {
                applicationFormData['org'] = companyName;
            }
        }
    }
    for (var _i = 0, _c = Object.entries(applicationFormData); _i < _c.length; _i++) {
        var _d = _c[_i], fieldName = _d[0], value = _d[1];
        var $field = $("input[name='" + fieldName + "']");
        if (!value || !$field || $field.val()) {
            continue;
        }
        $field.val(value.trim());
    }
}
function receiveData(data) {
    if (!data || receivedData) {
        return;
    }
    data.textKernelLocation = linkedInLocationToTextKernel(data.location);
    data._v = 3;
    receivedData = data;
    overlayButton.hideMask();
    if (userHasClicked) {
        fillApplicationForm(receivedData);
        overlayButton.setState('completed');
    }
    else {
        overlayButton.setState('ready');
    }
}
function awliEventHandler(event) {
    if (event.origin !== MESSAGE_ORIGIN) {
        return;
    }
    var payload = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
    switch (payload.method) {
        case 'awliOAuth':
            userHasClicked = true;
            break;
        case 'ready':
            overlayButton.setState('ready');
            overlayButton.showMask();
            break;
    }
}
window._awliReceiveData = receiveData;
window.addEventListener('message', awliEventHandler);
//# sourceMappingURL=awliV3.js.map