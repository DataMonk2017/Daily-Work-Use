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

If the rules are equal in specificity (in this case they are), individual rules get overridden in the order they're defined in the CSS, so in your example red wins because it comes later in the CSS definitions. The same rule applies in other cases as well, for example:
```csss
<div class="red green">
```
Which of these wins?
```css
.green { color: green; }
.red { color: red; }
```
`.red` wins here, it doesn't matter the order in the `class` attribute, all that matters is the order the styles are defined in the CSS itself.
