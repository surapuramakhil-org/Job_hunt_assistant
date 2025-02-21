$(function () {
  $('.application-file-input').change(function () {
    var filename = $(this).val();
    var visibleUpload = $(this).parent();
    var filenameTarget = visibleUpload.children('.filename');
    var defaultLabel = visibleUpload.children('.default-label');
    if (filename) {
      filename = filename.replace('C:\\fakepath\\', '');
      filenameTarget.text(filename).show();
      visibleUpload.addClass('has-file');
      defaultLabel.hide();
    } else {
      visibleUpload.removeClass('has-file');
      filenameTarget.hide();
      defaultLabel.show();
    }
  });

  var requiredCheckboxes = $('.required-field :checkbox[required]');
  requiredCheckboxes.change(function () {
    if (requiredCheckboxes.is(':checked')) {
      requiredCheckboxes.removeAttr('required');
    } else {
      requiredCheckboxes.attr('required', 'required');
    }
  });
});

$('#show-veteran-info').on('click', function () {
  $('#veteran-info').slideToggle('slow');
});

$('#show-disability-info').on('click', function () {
  $('#disability-info').slideToggle('slow');
});

/*
 * EEO expandable descriptions will be showing by default on page render,
 * so that browsers without JavaScript enabled can still view them. Clicking
 * on an info icon will toggle the corresponding expandable description section.
 */
$(function () {
  $('.eeo-section .eeo-more-info-button').each(function () {
    if (this.dataset && this.dataset['expandSelector']) {
      $(this.dataset['expandSelector']).hide();
      $(this).attr('aria-expanded', false);
    }
  });
  $('.eeo-section .eeo-more-info-button').on('click', function (event) {
    if (!event) {
      return;
    }
    var target = event.delegateTarget;
    if (target && target.dataset && target.dataset['expandSelector']) {
      $(target.dataset['expandSelector']).slideToggle('slow', function () {
        var hidden = $(this).css('display') === 'none';
        /* Set aria-expanded on the info icon appropriately. */
        $(target).attr('aria-expanded', !hidden);
      });
    }
  });

  var disabilitySelectElement = $('#disabilitySelectElement')[0];
  if (disabilitySelectElement && !disabilitySelectElement.value) {
    $('#disabilitySignatureSection').hide();
  }

  $('#disabilitySelectElement').on('change', function (event) {
    if (!event.target) {
      return;
    }
    var hasValue = !!event.target.value;
    var signatureSection = $('#disabilitySignatureSection');
    var showingSignature = signatureSection.css('display') !== 'none';
    if (hasValue !== showingSignature) {
      signatureSection.slideToggle('slow');
    }
    signatureSection.find('input').prop('required', hasValue);
  });
});

$(function () {
  var standardPronounsOption = $('#candidatePronounsCheckboxes .standardPronounsOption');
  var useNameOnlyPronounsOption = $('#useNameOnlyPronounsOption');
  var customPronounsOption = $('#customPronounsOption');
  var customPronounsTextField = $('#customPronounsTextField');

  standardPronounsOption.on('change', function (event) {
    if (standardPronounsOption.is(':checked')) {
      useNameOnlyPronounsOption.prop('checked', false);
      customPronounsOption.prop('checked', false);
      customPronounsTextField.hide();
      customPronounsTextField.val('');
    }
  });

  useNameOnlyPronounsOption.on('change', function (event) {
    //uncheck all boxes when 'Use name only' is selected
    if (useNameOnlyPronounsOption.is(':checked')) {
      standardPronounsOption.prop('checked', false);
      customPronounsOption.prop('checked', false);
      //hide text field for custom pronouns & set it to be empty
      customPronounsTextField.hide();
      customPronounsTextField.val('');
    }
  });

  customPronounsOption.on('change', function (event) {
    if (customPronounsOption.is(':checked')) {
      useNameOnlyPronounsOption.prop('checked', false);
      standardPronounsOption.prop('checked', false);
      customPronounsTextField.show();
    } else {
      customPronounsTextField.hide();
      customPronounsTextField.val('');
    }
  });
});
