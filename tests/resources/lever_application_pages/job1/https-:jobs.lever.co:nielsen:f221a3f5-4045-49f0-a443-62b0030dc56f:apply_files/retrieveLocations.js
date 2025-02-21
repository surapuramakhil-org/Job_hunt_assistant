"use strict";
var SEARCH_DELAY = 500;
var LOCATION_MAX_SEARCH_LENGTH = 100;
var searchedLocations;
var debouncedGetLocationResultsByInput = debounce(getLocationResultsByInput, SEARCH_DELAY);
$(function () {
    $('input.location-input').on('input', function () {
        setDisplayCSS('.dropdown-container', true);
    });
    $('input.location-input').on('keydown', function (event) {
        var _a, _b, _c, _d, _e;
        if (((_a = event === null || event === void 0 ? void 0 : event.originalEvent) === null || _a === void 0 ? void 0 : _a.key) === 'ArrowLeft' || ((_b = event === null || event === void 0 ? void 0 : event.originalEvent) === null || _b === void 0 ? void 0 : _b.key) === 'ArrowRight') {
            return;
        }
        var activeOption = $('.dropdown-location.dropdown-location-active');
        var activeIndex = $('.dropdown-location').index(activeOption);
        var numOfOptions = $('.dropdown-location').length;
        if (((_c = event === null || event === void 0 ? void 0 : event.originalEvent) === null || _c === void 0 ? void 0 : _c.key) === 'ArrowDown') {
            handleArrowDown(event, activeOption, activeIndex, numOfOptions);
        }
        else if (((_d = event === null || event === void 0 ? void 0 : event.originalEvent) === null || _d === void 0 ? void 0 : _d.key) === 'ArrowUp') {
            handleArrowUp(event, activeOption, activeIndex, numOfOptions);
        }
        else if (((_e = event === null || event === void 0 ? void 0 : event.originalEvent) === null || _e === void 0 ? void 0 : _e.key) === 'Enter') {
            handleEnter(event, activeOption);
        }
        else {
            debouncedGetLocationResultsByInput();
        }
    });
    $('input.location-input').on('blur', function (event) {
        if ($(event.target).closest('.dropdown-location').length === 0 &&
            $('.dropdown-container').css('display') !== 'none') {
            setDisplayCSS('.dropdown-container', false);
            emptyDropdownContainer();
            $('input.location-input').val('');
            $('#selected-location').val('');
        }
    });
    $(document).on('mousedown', '.dropdown-location', function (event) {
        setDisplayCSS('.dropdown-container', false);
        $('input.location-input').val(event.target.textContent);
        var selectedIndex = event.target.id.split('-')[1];
        $('#selected-location').val(JSON.stringify(searchedLocations[selectedIndex]));
        emptyDropdownContainer();
    });
});
function addActiveClassToDropdownOption(index) {
    $('.dropdown-location').eq(index).addClass('dropdown-location-active');
}
function removeActiveClassFromDropdownOption(index) {
    $('.dropdown-location').eq(index).removeClass('dropdown-location-active');
}
function handleArrowDown(event, activeOption, activeIndex, numOfOptions) {
    event.preventDefault();
    if (activeOption.length > 0) {
        removeActiveClassFromDropdownOption(activeIndex);
        var nextIndex = activeIndex === numOfOptions - 1 ? 0 : activeIndex + 1;
        addActiveClassToDropdownOption(nextIndex);
    }
    else {
        addActiveClassToDropdownOption(0);
    }
}
function handleArrowUp(event, activeOption, activeIndex, numOfOptions) {
    event.preventDefault();
    if (activeOption.length > 0) {
        removeActiveClassFromDropdownOption(activeIndex);
        var previousIndex = activeIndex === 0 ? numOfOptions - 1 : activeIndex - 1;
        addActiveClassToDropdownOption(previousIndex);
    }
    else {
        addActiveClassToDropdownOption(numOfOptions - 1);
    }
}
function handleEnter(event, activeOption) {
    event.preventDefault();
    setDisplayCSS('.dropdown-container', false);
    $('input.location-input').val(activeOption.text());
    var activeOptionId = activeOption.attr('id');
    var selectedIndex = parseInt(activeOptionId.split('-')[1]);
    $('#selected-location').val(JSON.stringify(searchedLocations[selectedIndex]));
    emptyDropdownContainer();
}
function emptyDropdownContainer() {
    $('.dropdown-results').empty();
    setDisplayCSS('.dropdown-no-results', false);
    setDisplayCSS('.dropdown-loading-results', false);
    searchedLocations = undefined;
}
function parseData(data) {
    var parsedData;
    try {
        parsedData = JSON.parse(data);
    }
    catch (e) {
        return;
    }
    return parsedData;
}
function getLocationResultsByInput() {
    var _a;
    emptyDropdownContainer();
    var locationInputValue = (_a = $('input.location-input').val()) === null || _a === void 0 ? void 0 : _a.toString();
    if (locationInputValue) {
        if (!isValidSearchQuery(locationInputValue)) {
            setDisplayCSS('.dropdown-no-results', true);
            return;
        }
        setDisplayCSS('.dropdown-loading-results', true);
        var req_1 = new XMLHttpRequest();
        var encodedText = encodeURIComponent(locationInputValue);
        var hcaptchaResponse = $('#hcaptchaResponseInput').val();
        var searchLocationsUrl = "/searchLocations?text=".concat(encodedText, "&hcaptchaResponse=").concat(hcaptchaResponse);
        req_1.onreadystatechange = function () {
            if (req_1.readyState === 4) {
                setDisplayCSS('.dropdown-no-results', false);
                setDisplayCSS('.dropdown-loading-results', false);
                if (req_1.status === 200) {
                    searchedLocations = parseData(req_1.response);
                    searchedLocations === null || searchedLocations === void 0 ? void 0 : searchedLocations.forEach(function (location, index) {
                        $('.dropdown-results').append("<div class=\"break-word dropdown-location width-full py1 px2\" id=\"location-".concat(index, "\">").concat(location.name, "</div>"));
                    });
                }
                else {
                    searchedLocations = undefined;
                }
                if (!(searchedLocations === null || searchedLocations === void 0 ? void 0 : searchedLocations.length)) {
                    setDisplayCSS('.dropdown-no-results', true);
                }
            }
        };
        req_1.open('GET', searchLocationsUrl, true);
        req_1.send();
    }
}
function isValidSearchQuery(value) {
    return !!value && value.length <= LOCATION_MAX_SEARCH_LENGTH;
}
function setDisplayCSS(className, shouldDisplay) {
    $(className).css({
        display: shouldDisplay ? 'flex' : 'none',
    });
}
//# sourceMappingURL=retrieveLocations.js.map