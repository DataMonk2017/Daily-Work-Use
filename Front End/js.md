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
## make bootstrap thumbnail same size 
You can achieve that by defining dimensions for your containers.

for example in your container element(.thumbnail), set a specific dimensions to follow like:

```
.thumbnail{        
    width: 300px; 
    // or you could use percentage values for responsive layout
    // width : 100%;
    height: 500px;
    overflow: auto;
}

.thumbnail img{
    // your styles for the image
    width: 100%;
    height: auto;
    display: block;
}
```
and so on with the other elements.

##
[Stackoverlfow](https://stackoverflow.com/questions/8206565/check-uncheck-checkbox-with-javascript)

Check/Uncheck checkbox with JavaScript?

Javascript:
```
// Check
document.getElementById("checkbox").checked = true;

// Uncheck
document.getElementById("checkbox").checked = false;
```

jQuery (1.6+):
```
// Check
$("#checkbox").prop("checked", true);

// Uncheck
$("#checkbox").prop("checked", false);
```

jQuery (1.5-):
```
// Check
$("#checkbox").attr("checked", true);

// Uncheck
$("#checkbox").attr("checked", false);
```
