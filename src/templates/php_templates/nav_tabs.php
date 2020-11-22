<?php foreach($nav as $k => $tab) { ?>
    <li id="tab-<?php echo $k; ?>" class="tab">
        <a href="<?php echo $tab['url']; ?>" title="<?php echo $tab['title']; ?>"
        	class="<?php echo $tab['classes']; ?>"><?php echo $tab['label'];?></a>
    </li>
<?php } ?>
