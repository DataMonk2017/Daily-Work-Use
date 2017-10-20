# This file is used to keep my notes in css.
## 
Use a white space to match all descendants of an element:
```css
div.dropdown * {
    color: red;
}
```
x y matches every element y that is inside x, however deeply nested it may be - children, grandchildren and so on.
The asterisk * matches any element.


## 
set min-height to control height of element
```css
.div {
min-height:100%;
}
```


## 
remove default style from browsers
```css
html, body {
     font-size: 40px;      
     margin:0; /* remove default margin */
     padding:0; /* remove default padding */
     width:100%; /* take full browser width */
     height:100%; /* take full browser height*/
}
```


## 
A more specific rule will override a less-specific rule.
```css
a {
  /* css */
}
```
is normally overruled by:
```css
body div #elementID ul li a{
  /*css*/
}
```
If, however, you add !important to the less-specific selector's CSS declaration, it will have priority.

Using !important has its purposes (though I struggle to think of them), but it's much like using a nuclear explosion to stop the foxes killing your chickens; yes, the foxes will be killed, but so will the chickens. And the neighbourhood.

It also makes debugging your CSS a nightmare (from personal, empirical, experience).

##
One Sentence Conclusion: No matter the order in the 'class' attribute, what comes the latter in css will be applied and override the former rule.

Explanation:

If the rules are equal in specificity (in this case they are), individual rules get overridden in the order they're defined in the CSS, so in your example red wins because it comes later in the CSS definitions. The same rule applies in other cases as well, for example:
```html
<div class="red green">
```
Which of these wins?
```css
.green { color: green; }
.red { color: red; }
```
`.red` wins here, it doesn't matter the order in the `class` attribute, all that matters is the order the styles are defined in the CSS itself.

##

move the button to the right of `panel-heading`.
```html
<div class="panel panel-default">
    <div class="panel-heading clearfix">
      <h4 class="panel-title pull-left" style="padding-top: 7.5px;">Panel header</h4>
      <div class="btn-group pull-right">
        <a href="#" class="btn btn-default btn-sm">## Lock</a>
        <a href="#" class="btn btn-default btn-sm">## Delete</a>
        <a href="#" class="btn btn-default btn-sm">## Move</a>
      </div>
    </div>
    ...
</div>
```
## cellpadding and cellspacing

[StackOverflow](https://stackoverflow.com/questions/339923/set-cellpadding-and-cellspacing-in-css)

In an HTML table, the cellpadding and cellspacing can be set like this:
```
<table cellspacing="1" cellpadding="1">
```
How can the same be accomplished using CSS?
    
    
For controlling "cellpadding" in CSS, you can simply use padding on table cells.
For "cellspacing", you can apply the border-spacing CSS property to your table.
```
td {
padding: 10px;
}

table {
border-spacing: 10px;
border-collapes: seperate;
}
```

This will work in almost all popular browsers except for Internet Explorer up through Internet Explorer 7, where you're almost out of luck. I say "almost" because these browsers still support the border-collapse property, which merges the borders of adjoining table cells. If you're trying to eliminate `cellspacing` (that is, `cellspacing="0"`) then `border-collapse:collapse` should have the same effect: no space between table cells. This support is buggy, though, as it does not override an existing cellspacing HTML attribute on the table element.

In short: for non-Internet Explorer 5-7 browsers, `border-spacing` handles you. For Internet Explorer, if your situation is just right (you want 0 cellspacing and your table doesn't have it defined already), you can use `border-collapse:collapse`.
```
table { 
    border-spacing: 0;
    border-collapse: collapse;
}
```
Note: For a great overview of CSS properties that one can apply to tables and for which browsers, see this [fantastic Quirksmode page](https://quirksmode.org/css/css2/tables.html).

## arrow on dropdown menu

[StackOverflow](https://stackoverflow.com/questions/19983995/bootstrap-3-arrow-on-dropdown-menu)

```
.dropdown-menu:before {
  position: absolute;
  top: -7px;
  left: 9px;
  display: inline-block;
  border-right: 7px solid transparent;
  border-bottom: 7px solid #ccc;
  border-left: 7px solid transparent;
  border-bottom-color: rgba(0, 0, 0, 0.2);
  content: '';
}

.dropdown-menu:after {
  position: absolute;
  top: -6px;
  left: 10px;
  display: inline-block;
  border-right: 6px solid transparent;
  border-bottom: 6px solid #ffffff;
  border-left: 6px solid transparent;
  content: '';
}
```
Confused how? [See here for an animation that explains css triangles.](https://codepen.io/chriscoyier/pen/lotjh)

Just to follow up on this - if you want the arrow to position itself correctly (like when using it on a navbar element that is right-aligned, you need the following additional CSS to ensure the arrow is right-aligned:
```
.navbar .navbar-right > li > .dropdown-menu:before,
.navbar .nav > li > .dropdown-menu.navbar-right:before {
    right: 12px; left: auto;
}

.navbar .navbar-right > li > .dropdown-menu:after,
.navbar .nav > li > .dropdown-menu.navbar-right:after {
    right: 13px; left: auto;
}
```
Note the "navbar-right" - that was introduced in BS3 instead of pull-right for navbars.

Remvoe the arrow:
```
.dropdown-menu:after {
    border: none !important;
    content: "" !important;
}
.dropdown-menu:before {
    border: none !important;
    content: "" !important;
}
```

## Bootstrap dropdown: position of dropdown content
Edit:

As of v3.1.0, we've deprecated .pull-right on dropdown menus. To right-align a menu, use .dropdown-menu-right. Right-aligned nav components in the navbar use a mixin version of this class to automatically align the menu. To override it, use .dropdown-menu-left.

You can use the 'dropdown-right' class to line the right hand side of the menu up with the caret:
```
<li class="dropdown">
  <a class="dropdown-toggle" href="#">Link</a>
  <ul class="dropdown-menu dropdown-menu-right">
     <li>...</li>
  </ul>
</li>
```
When Bootstrap < 3.1.0 but you should generally be using the above (and if it doesn't seem to be working double check the version number of Bootstrap that you're including)!

You can use the 'pull-right' class to line the right hand side of the menu up with the caret:
```
<li class="dropdown">
  <a class="dropdown-toggle" href="#">Link</a>
  <ul class="dropdown-menu pull-right">
     <li>...</li>
  </ul>
</li>
```

## calc usage

[CSS-Trick](https://css-tricks.com/a-couple-of-use-cases-for-calc/#article-header-id-1)
