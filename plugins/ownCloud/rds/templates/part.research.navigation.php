<!-- translation strings -->
<div style="display:none" id="new-research-string"><?php p($l->t('New connection')); ?></div>
<div style="display:none" id="save-not-finished"><?php p($l->t('Your entries could not be saved.')); ?></div>

<script id="navigation-tpl" type="text/x-handlebars-template">
    <li id="new-research"><a href="#"><?php p($l->t('Add connection')); ?></a></li>
    {{#each studies}}
        <li class="connection with-menu {{#if active}}active{{/if}}"  data-id="{{ researchIndex }}">
            <a href="#">Project {{ researchIndex }}</a>
            <div class="app-navigation-entry-utils">
                <ul>
                    <li class="app-navigation-entry-utils-menu-button svg"><button></button></li>
                </ul>
            </div>

            <div class="app-navigation-entry-menu">
                <ul>
                    <li><button class="delete icon-delete svg" title="delete"></button></li>
                </ul>
            </div>
        </li>
    {{/each}}
</script>

<ul></ul>