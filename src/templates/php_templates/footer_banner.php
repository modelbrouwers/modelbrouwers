<ul>
    <?php foreach($footer_shop as $id => $li_data) { ?>
        <li>
            <a class="aankeiler" href="<?php echo $li_data['url']; ?>"><?php echo $li_data['text']; ?></a>
            <div id="footer-<?php echo $id; ?>" class="blokje">
                <a class="div_link" href="<?php echo $li_data['url']; ?>"></a>
            </div>
        </li>
    <?php } ?>
</ul>
<img src="<?php echo $storage->url('images/logo/tekst.gif');?>" width="773" height="52" alt="logo Modelbrouwers" />
