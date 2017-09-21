# This file is used for saving my notes in css.
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
