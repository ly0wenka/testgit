/**
 * File navigation.js.
 *
 * Handles toggling the navigation menu for small screens and enables TAB key
 * navigation support for dropdown menus.
 */
( function() {
	var container, button, menu, links, i, len;

	container = document.getElementById( 'site-navigation' );
	if ( ! container ) {
		return;
	}

	button = container.getElementsByTagName( 'button' )[0];
	if ( 'undefined' === typeof button ) {
		return;
	}

	menu = container.getElementsByTagName( 'ul' )[0];

	// Hide menu toggle button if menu is empty and return early.
	if ( 'undefined' === typeof menu ) {
		button.style.display = 'none';
		return;
	}

	menu.setAttribute( 'aria-expanded', 'false' );
	if ( -1 === menu.className.indexOf( 'nav-menu' ) ) {
		menu.className += ' nav-menu';
	}

	button.onclick = function() {
		if ( -1 !== container.className.indexOf( 'toggled' ) ) {
			container.className = container.className.replace( ' toggled', '' );
			button.setAttribute( 'aria-expanded', 'false' );
			menu.setAttribute( 'aria-expanded', 'false' );
		} else {
			container.className += ' toggled';
			button.setAttribute( 'aria-expanded', 'true' );
			menu.setAttribute( 'aria-expanded', 'true' );
		}
	};

	// Get all the link elements within the menu.
	links    = menu.getElementsByTagName( 'a' );

	// Each time a menu link is focused or blurred, toggle focus.
	for ( i = 0, len = links.length; i < len; i++ ) {
		links[i].addEventListener( 'focus', toggleFocus, true );
		links[i].addEventListener( 'blur', toggleFocus, true );
	}

	/**
	 * Sets or removes .focus class on an element.
	 */
	function toggleFocus() {
		var self = this;

		// Move up through the ancestors of the current link until we hit .nav-menu.
		while ( -1 === self.className.indexOf( 'nav-menu' ) ) {

			// On li elements toggle the class .focus.
			if ( 'li' === self.tagName.toLowerCase() ) {
				if ( -1 !== self.className.indexOf( 'focus' ) ) {
					self.className = self.className.replace( ' focus', '' );
				} else {
					self.className += ' focus';
				}
			}

			self = self.parentElement;
		}
	}

	/**
	 * Toggles `focus` class to allow submenu access on tablets.
	 */
	( function( container ) {
		var touchStartFn, i,
			parentLink = container.querySelectorAll( '.menu-item-has-children > a, .page_item_has_children > a' );

		if ( 'ontouchstart' in window ) {
			touchStartFn = function( e ) {
				var menuItem = this.parentNode, i;

				if ( ! menuItem.classList.contains( 'focus' ) ) {
					e.preventDefault();
					for ( i = 0; i < menuItem.parentNode.children.length; ++i ) {
						if ( menuItem === menuItem.parentNode.children[i] ) {
							continue;
						}
						menuItem.parentNode.children[i].classList.remove( 'focus' );
					}
					menuItem.classList.add( 'focus' );
				} else {
					menuItem.classList.remove( 'focus' );
				}
			};

			for ( i = 0; i < parentLink.length; ++i ) {
				parentLink[i].addEventListener( 'touchstart', touchStartFn, false );
			}
		}
	}( container ) );
} )();

/**
 * Menu Navigation
 */
( function() {

	'use strict';

	jQuery(document).ready(function($){
		jQuery( window ).on( 'load.universityHub resize.universityHub', function() {
			if ( window.innerWidth < 1200 ) {
				jQuery('#main-navigation').on('focusout', function () {
					var $elem = jQuery(this);

				    // let the browser set focus on the newly clicked elem before check
				    setTimeout(function () {
				        if ( ! $elem.find(':focus').length ) {
				            jQuery( '#main-navigation #menu-toggle' ).trigger('click');
				        }
				    }, 0);
				});
			}
		} );

		/* Menu */
		var body, mainNav, topNav, menuToggle, siteNavigation, topMenuToggle, topSiteNavigation;

		function initMainNavigation( container ) {

			// Add dropdown toggle that displays child menu items.
			var dropdownToggle = $( '<button />', { 'class': 'dropdown-toggle', 'aria-expanded': false })
				.append( $( '<span />', { 'class': 'screen-reader-text', text: universityHubOptions.screenReaderText.expand }) );

			container.find( '.menu-item-has-children > a, .page_item_has_children > a' ).after( dropdownToggle );

			// Toggle buttons and submenu items with active children menu items.
			container.find( '.current-menu-ancestor > button' ).addClass( 'toggled-on' );
			container.find( '.current-menu-ancestor > .sub-menu' ).addClass( 'toggled-on' );

			// Add menu items with submenus to aria-haspopup="true".
			container.find( '.menu-item-has-children, .page_item_has_children' ).attr( 'aria-haspopup', 'true' );

			container.find( '.dropdown-toggle' ).on( 'click', function( e ) {
				var _this            = $( this ),
					screenReaderSpan = _this.find( '.screen-reader-text' );

				e.preventDefault();
				_this.toggleClass( 'toggled-on' );

				// jscs:disable
				_this.attr( 'aria-expanded', _this.attr( 'aria-expanded' ) === 'false' ? 'true' : 'false' );
				// jscs:enable
				screenReaderSpan.text( screenReaderSpan.text() === universityHubOptions.screenReaderText.expand ? universityHubOptions.screenReaderText.collapse : universityHubOptions.screenReaderText.expand );
			} );
		}

		mainNav = $( '#main-nav' );
		initMainNavigation( mainNav );

		/**
		 * Main Nav
		 */
		menuToggle       = mainNav.find( '.menu-toggle' );
		siteNavigation   = mainNav.find( '#site-navigation' );

		// Enable menuToggle.
		( function() {

			// Assume the initial scroll position is 0.
			var scroll = 0;

			// Return early if menuToggle is missing.
			if ( ! menuToggle.length ) {
				return;
			}

			menuToggle.on( 'click.universityHub', function() {
				// jscs:disable
				$( this ).add( siteNavigation ).attr( 'aria-expanded', $( this ).add( siteNavigation ).attr( 'aria-expanded' ) === 'false' ? 'true' : 'false' );
				// jscs:enable
			} );


			// Add an initial values for the attribute.
			menuToggle.add( siteNavigation ).attr( 'aria-expanded', 'false' );

			// Wait for a click on one of our menu toggles.
			menuToggle.on( 'click.universityHub', function() {

				// Assign this (the button that was clicked) to a variable.
				var button = this;

				// Gets the actual menu (parent of the button that was clicked).
				var menu = $( this ).parents( '.menu-wrapper' );

				// Remove selected classes from other menus.
				$( menuToggle ).not( button ).removeClass( 'selected' );
				$( '.menu-wrapper' ).not( menu ).removeClass( 'is-open' );

				// Toggle the selected classes for this menu.
				$( button ).toggleClass( 'selected' );
				$( menu ).toggleClass( 'is-open' );

				// Is the menu in an open state?
				var is_open = $( menu ).hasClass( 'is-open' );

				// If the menu is open and there wasn't a menu already open when clicking.
				if ( is_open && ! jQuery( 'body' ).hasClass( 'menu-open' ) ) {

					// Get the scroll position if we don't have one.
					if ( 0 === scroll ) {
						scroll = $( 'body' ).scrollTop();
					}

					// Add a custom body class.
					$( 'body' ).addClass( 'menu-open' );

				// If we're closing the menu.
				} else if ( ! is_open ) {
					$( 'body' ).removeClass( 'menu-open' );
					$( 'body' ).scrollTop( scroll );
					scroll = 0;
				}
			} );

			// Close menus when somewhere else in the document is clicked.
			$( document ).on( 'click touchstart', function() {
				$( 'body' ).removeClass( 'menu-open' );
				$( menuToggle ).removeClass( 'selected' );
				$( '.menu-wrapper' ).removeClass( 'is-open' );
			} );

			// Stop propagation if clicking inside of our main menu.
			$( '#main-nav' ).on( 'click touchstart', function( e ) {
				e.stopPropagation();
			} );
		} )();

		// Fix sub-menus for touch devices and better focus for hidden submenu items for accessibility.
		( function() {
			if ( ! siteNavigation.length || ! siteNavigation.children().length ) {
				return;
			}

			// Toggle `focus` class to allow submenu access on tablets.
			function toggleFocusClassTouchScreen() {
				if ( window.innerWidth >= 910 ) {
					$( document.body ).on( 'touchstart.universityHub', function( e ) {
						if ( ! $( e.target ).closest( '.main-navigation li' ).length ) {
							$( '.main-navigation li' ).removeClass( 'focus' );
						}
					} );
					siteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' ).on( 'touchstart.universityHub', function( e ) {
						var el = $( this ).parent( 'li' );

						if ( ! el.hasClass( 'focus' ) ) {
							e.preventDefault();
							el.toggleClass( 'focus' );
							el.siblings( '.focus' ).removeClass( 'focus' );
						}
					} );
				} else {
					siteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' ).unbind( 'touchstart.universityHub' );
				}
			}

			if ( 'ontouchstart' in window ) {
				$( window ).on( 'resize.universityHub', toggleFocusClassTouchScreen );
				toggleFocusClassTouchScreen();
			}

			siteNavigation.find( 'a' ).on( 'focus.universityHub blur.universityHub', function() {
				$( this ).parents( '.menu-item, .page_item' ).toggleClass( 'focus' );
			} );

			$('.main-navigation button.dropdown-toggle').on( 'click',function() {
				$(this).toggleClass('active');
				$(this).parent().find('.children, .sub-menu').first().toggleClass('toggled-on');
			});
		} )();

		/**
		 * Top Nav
		 */
		topNav = $( '#top-nav' );
		initMainNavigation( topNav );


		topMenuToggle       = topNav.find( '.menu-toggle' );
		topSiteNavigation   = topNav.find( '#site-top-navigation' );

		// Enable topMenuToggle.
		( function() {

			// Assume the initial scroll position is 0.
			var scroll = 0;

			// Return early if topMenuToggle is missing.
			if ( ! topMenuToggle.length ) {
				return;
			}

			topMenuToggle.on( 'click.universityHub', function() {
				// jscs:disable
				$( this ).add( topSiteNavigation ).attr( 'aria-expanded', $( this ).add( topSiteNavigation ).attr( 'aria-expanded' ) === 'false' ? 'true' : 'false' );
				// jscs:enable
			} );


			// Add an initial values for the attribute.
			topMenuToggle.add( topSiteNavigation ).attr( 'aria-expanded', 'false' );

			// Wait for a click on one of our menu toggles.
			topMenuToggle.on( 'click.universityHub', function() {

				// Assign this (the button that was clicked) to a variable.
				var button = this;

				// Gets the actual menu (parent of the button that was clicked).
				var menu = $( this ).parents( '.menu-wrapper' );

				// Remove selected classes from other menus.
				$( topMenuToggle ).not( button ).removeClass( 'selected' );
				$( '.menu-wrapper' ).not( menu ).removeClass( 'is-open' );

				// Toggle the selected classes for this menu.
				$( button ).toggleClass( 'selected' );
				$( menu ).toggleClass( 'is-open' );

				// Is the menu in an open state?
				var is_open = $( menu ).hasClass( 'is-open' );

				// If the menu is open and there wasn't a menu already open when clicking.
				if ( is_open && ! jQuery( 'body' ).hasClass( 'menu-open' ) ) {

					// Get the scroll position if we don't have one.
					if ( 0 === scroll ) {
						scroll = $( 'body' ).scrollTop();
					}

					// Add a custom body class.
					$( 'body' ).addClass( 'menu-open' );

				// If we're closing the menu.
				} else if ( ! is_open ) {
					$( 'body' ).removeClass( 'menu-open' );
					$( 'body' ).scrollTop( scroll );
					scroll = 0;
				}
			} );

			// Close menus when somewhere else in the document is clicked.
			$( document ).on( 'click touchstart', function() {
				$( 'body' ).removeClass( 'menu-open' );
				$( topMenuToggle ).removeClass( 'selected' );
				$( '.menu-wrapper' ).removeClass( 'is-open' );
			} );

			// Stop propagation if clicking inside of our main menu.
			$( '#top-nav' ).on( 'click touchstart', function( e ) {
				e.stopPropagation();
			} );
		} )();

		// Fix sub-menus for touch devices and better focus for hidden submenu items for accessibility.
		( function() {
			if ( ! topSiteNavigation.length || ! topSiteNavigation.children().length ) {
				return;
			}

			// Toggle `focus` class to allow submenu access on tablets.
			function topNavToggleFocusClassTouchScreen() {
				if ( window.innerWidth >= 910 ) {
					$( document.body ).on( 'touchstart.universityHub', function( e ) {
						if ( ! $( e.target ).closest( '.top-navigation li' ).length ) {
							$( '.top-navigation li' ).removeClass( 'focus' );
						}
					} );
					topSiteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' ).on( 'touchstart.universityHub', function( e ) {
						var el = $( this ).parent( 'li' );

						if ( ! el.hasClass( 'focus' ) ) {
							e.preventDefault();
							el.toggleClass( 'focus' );
							el.siblings( '.focus' ).removeClass( 'focus' );
						}
					} );
				} else {
					topSiteNavigation.find( '.menu-item-has-children > a, .page_item_has_children > a' ).unbind( 'touchstart.universityHub' );
				}
			}

			if ( 'ontouchstart' in window ) {
				$( window ).on( 'resize.universityHub', topNavToggleFocusClassTouchScreen );
				topNavToggleFocusClassTouchScreen();
			}

			topSiteNavigation.find( 'a' ).on( 'focus.universityHub blur.universityHub', function() {
				$( this ).parents( '.menu-item, .page_item' ).toggleClass( 'focus' );
			} );

			$('.top-navigation button.dropdown-toggle' ).on( 'click',function() {
				$(this).toggleClass('active');
				$(this).parent().find('.children, .sub-menu').first().toggleClass('toggled-on');
			});
		})();
	});
} )();
