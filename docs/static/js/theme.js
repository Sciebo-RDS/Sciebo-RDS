/*
Namespace for docs site
*/
var DocsTheme = {

  init: function() {
    this.initSidebar();
    this.initScrollspy();
    this.initTabbedBlocks();
    this.initToc();
    this.initCopyCode();
    this.initCopyAnchors();
  },

  initSidebar: function() {
    //sidebar dropdown menu
    $('#sidebar .sub-menu > a').click(function () {
      var above = $(this).prev('.sub-menu');
      // Toggle current submenu
      var sub = $(this).next();
      if (sub.is(":visible")) {
        $('.menu-arrow', this).addClass('fa-angle-right');
        $('.menu-arrow', this).removeClass('fa-angle-down');
        sub.slideUp(200);
        $(sub).removeClass("open");
        $(this).prev('.sub-menu').removeClass('open');
      } else {
        $('.menu-arrow', this).addClass('fa-angle-down');
        $('.menu-arrow', this).removeClass('fa-angle-right');
        sub.slideDown(200);
        $(sub).addClass("open");
        $(this).prev('.sub-menu').addClass('open');
      }
    });

    $('.toggle-nav').on('click', function(event) {
      console.log('toggle nav clicked');
      $('#sidebar').addClass('show-sidebar');
      $('#sidebar .sidebar-nav').addClass('show-sidebar-nav');
    });
    $('#close-button').on('click', function(event) {
      console.log('close menu clicked');
      $('#sidebar').removeClass('show-sidebar');
      $('#sidebar .sidebar-nav').removeClass('show-sidebar-nav');
    });
  },

  initScrollspy: function() {
    // poor man's scrollspy ;)
    var lastId,
      topMenu = $("#TableOfContents"),
      topMenuHeight = topMenu.outerHeight()+15,
      // All list items
      menuItems = topMenu.find("a"),
      // Anchors corresponding to menu items
      scrollItems = menuItems.map(function(){
        var item = $($(this).attr("href"));
        if (item.length) { return item; }
      });

      // Bind click handler to menu items
      // so we can get a fancy scroll animation
      menuItems.click(function(e){
        var href = $(this).attr("href"),
            offsetTop = href === "#" ? 0 : $(href).offset().top - $('.navbar').outerHeight() - 20;//-topMenuHeight+100;
        $('html, body').stop().animate({
            scrollTop: offsetTop
        }, 300);
        e.preventDefault();
      });

      // Bind to scroll
      $(window).scroll(function(){
         // affix toc]
         var totHeight = $('.navbar').outerHeight() + $('.article-tagline').outerHeight();
         console.log("totHeight: " + totHeight);
         if ($(this).scrollTop() > totHeight) {
           $('#TableOfContents').addClass('floating');
         } else {
           $('#TableOfContents').removeClass('floating');
         }

         console.log("navbar height: "+ $('.navbar').outerHeight());
         if ($(this).scrollTop() > $('.navbar').outerHeight()) {
           $('#sidebar').addClass('floating');
         } else {
           $('#sidebar').removeClass('floating');
         }
         // Get container scroll position
         var fromTop = $(this).scrollTop()+topMenuHeight;

         var cur = scrollItems.map(function(){
           if ($(this).offset().top < fromTop)
             return this;
         });
         // Get the id of the current element
         cur = cur[cur.length-1];
         var id = cur && cur.length ? cur[0].id : "";

         if (lastId !== id) {
             lastId = id;
             // Set/remove active class
             menuItems
               .parent().removeClass("active")
               .end().filter("[href='#"+id+"']").parent().addClass("active");
         }
      });
    },

    initTabbedBlocks: function() {
      // set up tabbed code blocks
      $('.tab-content').find('.tab-pane').each(function(idx, item) {
        var navTabs = $(this).closest('.code-tabs').find('.nav-tabs'),
            title = $(this).attr('title');
        navTabs.append('<li><a href="#">'+title+'</a></li');
      });

      $('.code-tabs ul.nav-tabs').each(function() {
        $(this).find("li:first").addClass('active');
      })

      $('.code-tabs .tab-content').each(function() {
        // $(item).find('tab-pane').addClass('active');
        $(this).find("div:first").addClass('active');
      });

      $('.nav-tabs a').click(function(e){
        e.preventDefault();
        var tab  = $(this).parent(),
            tabIndex = tab.index(),
            tabPanel = $(this).closest('.code-tabs'),
            tabPane = tabPanel.find('.tab-pane').eq(tabIndex);
        tabPanel.find('.active').removeClass('active');
        tab.addClass('active');
        tabPane.addClass('active');
      });

      // todo - optimize and make less terrible
      $('.code-tabs').each(function() {
        var largest = 0;
        var codeHeight = 0;
        var panes = $(this).find('.tab-pane');
        panes.each(function() {
          var outerHeight = $(this).outerHeight();
          console.log("outerHeight: " + outerHeight);
          if (outerHeight > largest) {
            largest = outerHeight;
            codeHeight = $(this).find('code').outerHeight();
          }
        });
        console.log("codeHeight: " + codeHeight);
        panes.each(function() {
          $(this).height(largest);
          // make all the <code> elements the same height to
          // avoid it jumping around when switching tabs
          $(this).find('code').height(largest - 5);
        });
      });
    },

    initCopyCode: function() {

      $('pre code').each(function() {
        var code = $(this);
        code.after('<span class="copy-to-clipboard">Copy</span>');
        code.on('mouseenter', function() {
          var copyBlock = $(this).next('.copy-to-clipboard');
          copyBlock.addClass('copy-active');
        });
        code.on('mouseleave', function() {
          var copyBlock = $(this).next('.copy-to-clipboard');
          copyBlock.removeClass('copy-active');
          copyBlock.html("Copy");
        });
      });

      var text, clip = new Clipboard('.copy-to-clipboard', {
        text: function(trigger) {
          return $(trigger).prev('code').text();
        }
      });

      clip.on('success', function(e) {
        e.clearSelection();
        console.log("copied!");
        $(e.trigger).html("Copied!");
      });

      clip.on('error', function(e) {
        console.log("error: " + e);
      });
    },

    initCopyAnchors: function() {
      $("h2").append(function(index, html){
        var element = $(this);
        var url = document.location.origin + document.location.pathname;
        var link = url + "#"+element[0].id;
        return " <span class='anchor'><a href='"+link+"'>" +
          "<i class='fa fa-link fa-lg'></i></a></span>"
        ;
      });
    },

    initToc: function() {
      // Hugo gives back a stupidly structured nav structure :shrug:
      var toc = $('#TableOfContents > ul > li > ul');
      toc.prepend('<li class="toc-label">Contents</li>')
    }
};

$(document).ready(function() {
  DocsTheme.init();
});


// disable code block for mermaid
jQuery(document).ready(function() {
  $('code.language-mermaid').each(function(index, element) {
    var content = $(element).html().replace(/&amp;/g, '&');
    $(element).parent().replaceWith('<div class="mermaid" align="center">' + content + '</div>');
  });
});