<ul>
    <?php foreach($footer_shop as $id => $li_data) { ?>
        <li>
            <a class="aankeiler" href="<?php echo $li_data['url']; ?>"><?php echo $li_data['text']; ?></a>
            <div id="footer-<?php echo $id; ?>" class="blokje">
                <a class="div_link" href="<?php echo $li_data['url']; ?>"></a>
            </div>
        </li>
    <?php } ?>
        <!-- <li id="new_product">
            <div>
                <iframe src="/shop/catalog/products_new_small2.php"
                name="whats_new" scrolling="no"
                frameborder="0" width="135px" height="163px">
                </iframe>
            </div>
        </li> -->
</ul>
<img src="<?php echo $storage->url('images/logo/tekst.gif');?>" width="773" height="52" alt="logo Modelbrouwers" />