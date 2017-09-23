You can compare DIV width with scrollWidth to detect if text is overflowing:
```javascript
if ($('.less')[0].scrollWidth <= $('.less').width()) {
   $(".text-size").hide();
}
```

Looks like your requirement is just to fade out the text beginning at a certain height (about 150px), the text (if any) presenting at that height is considered as overflow. So you can try using some kind of transparent linear gradient layer placed on top of the text area, we can achieve this in a neat way using the pseudo-element :before like this:
```css
.row:before {
  content:'';
  width:100%;
  height:100%;    
  position:absolute;
  left:0;
  top:0;
  background:linear-gradient(transparent 150px, white);
}
```
