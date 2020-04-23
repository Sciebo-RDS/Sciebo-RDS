<?php
style( 'rds', array( 'style', 'tooltipster.bundle.min' ) );
script( 'rds', array( 'handlebars', 'tooltipster.bundle.min', 'tooltipster-SVG.min' ) );

script( 'rds', array( 'Studies', 'Metadata', 'Services', 'View', 'Files', 'main-rds' ) );

?>

<div id = 'app'>
<div id = 'app-navigation'>
<?php print_unescaped( $this->inc( 'part.research.navigation' ) );
?>
<?php print_unescaped( $this->inc( 'part.research.settings' ) );
?>
</div>

<div id = 'app-content'></div>
</div>

<script id = 'research-overview-tpl' type = 'text/x-handlebars-template'>
<?php print_unescaped( $this->inc( 'part.research.content.overview' ) );
?>
</script>

<script id = 'research-edit-service-tpl' type = 'text/x-handlebars-template'>
<?php print_unescaped( $this->inc( 'part.research.content.service' ) );
?>
</script>

<script id = 'research-edit-metadata-tpl' type = 'text/x-handlebars-template'>
<?php print_unescaped( $this->inc( 'part.research.content.metadata' ) );
?>
</script>

<script id = 'research-edit-file-tpl' type = 'text/x-handlebars-template'>
<?php print_unescaped( $this->inc( 'part.research.content.file' ) );
?>
</script>
