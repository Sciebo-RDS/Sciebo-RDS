<?php
script( 'rds', 'handlebars' );
script( 'rds', 'connections' );
style( 'rds', 'style' );
?>

<div id="app">
  <div id="app-navigation">
    <?php print_unescaped( $this->inc( 'part.connect.navigation' ) ); ?>
    <?php print_unescaped( $this->inc( 'part.connect.settings' ) ); ?>
  </div>

  <div id="app-content"></div>
</div>

<script id="connection-overview-tpl" type="text/x-handlebars-template">
  <?php print_unescaped( $this->inc( 'part.connect.content' ) );
  ?>
</script>

<script id="connection-edit-service-tpl" type="text/x-handlebars-template">
  <?php print_unescaped( $this->inc( 'part.connect.connection.service' ) );
  ?>
</script>

<script id="connection-edit-metadata-tpl" type="text/x-handlebars-template">
  <?php print_unescaped( $this->inc( 'part.connect.connection.metadata' ) );
  ?>
</script>

<script id="connection-edit-file-tpl" type="text/x-handlebars-template">
  <?php print_unescaped( $this->inc( 'part.connect.connection.file' ) );
  ?>
</script>
