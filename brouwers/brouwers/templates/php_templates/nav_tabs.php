<ul id="tabs">
    <?php foreach($nav as $k => $tab) { ?>
        <li id="<?php echo $k ?>">
            <?php echo "<a href=\"{$tab['url']}\" title=\"{$tab['alt']}\">"; ?>
                <img src="<?php echo $settings['STATIC_URL'].$tab['img']; ?>" alt="<?php echo $k; ?>" /></a>
        </li>
    <?php } ?>
    <!--<li>
        <img src="{{ STATIC_URL }}images/nav/modelbouw_wiki.png" alt="Modelbouw Wiki"/>
    </li>-->
</ul>
