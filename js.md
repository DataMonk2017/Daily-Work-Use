You can compare DIV width with scrollWidth to detect if text is overflowing:
```javascript
if ($('.less')[0].scrollWidth <= $('.less').width()) {
   $(".text-size").hide();
}
```
