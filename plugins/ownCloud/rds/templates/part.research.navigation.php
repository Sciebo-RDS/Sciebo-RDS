<script id="navigation-tpl" type="text/x-handlebars-template">
    <li id="new-research"><a href="#"><?php p($l->t('Add research')); ?></a></li>
    {{#each studies}}
        <li class="research with-menu {{#if active}}active{{/if}}"  data-id="{{ researchIndex }}">
            <a href="#"><?php p($l->t('Project')); ?> {{ researchIndex }}</a>
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