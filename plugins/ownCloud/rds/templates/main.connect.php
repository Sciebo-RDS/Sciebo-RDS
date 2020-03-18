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

  <div id="app-content">
    <div id="app-content-wrapper">
      <div id="connection-overview">
        <?php print_unescaped( $this->inc( 'part.connect.content' ) ); ?>
      </div>

      <div id="connection-edit-service">
        <?php print_unescaped($this->inc('part.connect.connection.service')); ?>
      </div>

      <div id="connection-edit-metadata">
        <?php print_unescaped($this->inc('part.connect.connection.metadata'));
        ?>
      </div>

      <div id="connection-edit-file">
        <?php print_unescaped($this->inc('part.connect.connection.file')); ?>
      </div>
    </div>
  </div>
</div>
