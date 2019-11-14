// Copy to clipboard uses clipboard.js (https://clipboardjs.com/)
// and parts of Primer for tooltip support
var copyCode = {
  init: function() {
    $('pre [class^=language]').each(function() {
      $(this).after('<span class="copy-btn" data-clipboard-snippet></span>');
      // $(this).prepend('<button class="copy-btn" data-clipboard-snippet></button>');
    });
    var clipboardSnippets = new Clipboard('[data-clipboard-snippet]',{
      target: function(trigger) {
        return trigger.nextElementSibling;
      }
    });
    clipboardSnippets.on('success', function(e) {
      e.clearSelection();
      copyCode.showTooltip(e.trigger, 'Copied to clipboard');
    });
    clipboardSnippets.on('error', function(e) {
      copyCode.showTooltip(e.trigger, copyCode.fallbackMessage());
    });

    $('.copy-btn').each(function() {
      $(this).mouseenter(function() {
        copyCode.showTooltip(this, 'Click to copy');
      });
      $(this).mouseleave(function() {
        $(this).removeAttr('aria-label');
        $(this).removeClass('tooltipped tooltipped-nw');
      });
    });
  },

  showTooltip: function(elem, msg) {
    $(elem).addClass('tooltipped tooltipped-nw');
    $(elem).attr('aria-label', msg);
  },

  fallbackMessage: function() {
    var actionMsg = '';
    if (/iPhone|iPad/i.test(navigator.userAgent)) {
      actionMsg = 'No support :(';
    } else if (/Mac/i.test(navigator.userAgent)) {
      actionMsg = 'Press ⌘-C to copy';
    } else {
      actionMsg = 'Press Ctrl-C to copy';
    }
    return actionMsg;
  }
};

$(document).ready(copyCode.init);
