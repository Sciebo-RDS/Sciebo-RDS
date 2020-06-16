<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Port extends Entity implements JsonSerializable {

    protected $port;
    protected $properties;

    function __construct() {
        $this->properties = [];
    }

    /**
    * value can be a boolean or array. The element of value has to be an assoc array with the keys 'key' and 'value'.
    * @param string portType
    * @param [boolean, array] value
    * @return NULL
    *
    * Example: ['portType'=>'CustomProperties', 'value'=> [['key'=>'serviceproject', 'value'=>'testproject']]]
    */

    public function addProperty( $portType, $value ) {
        $index = $this->getIndexOfProperty( $portType );

        if ( $index != NULL ) {
            $this->properties[$index] = ['portType'=>$portType, 'value'=>$value];
        } else {
            $this->properties[] = ['portType'=>$portType, 'value'=>$value];
        }
    }

    public function removeProperty( $portType ) {
        $index = $this->getIndexOfProperty( $portType );

        if ( $index != NULL ) {
            unset( $this->properties[$index] );
        }
    }

    public function hasProperty( $portType ) {
        $index = $this->getIndexOfProperty( $portType );

        if ( $index != NULL ) {
            return True;
        }
        return False;
    }

    public function equal( $port ) {
        return ( $this->jsonSerialize() == $port->jsonSerialize() );
    }

    public function notEqualPropertyIndices( $port ) {
        $returnList = [];

        foreach ( $port->properties as $prop ) {
            $index = $this->getIndexOfProperty( $prop['portType'] );

            if ( $index == NULL || $this->properties[$index]['value'] != $prop['value'] ) {
                $returnList[] = $index;
            }
        }

        return $returnList;
    }

    private function getIndexOfProperty( $portType ) {
        $index = NULL;
        $i = 0;
        foreach ( $this->properties as $prop ) {
            if ( $prop['portType'] == $portType ) {
                $index = $i;
                break;
            }
            $i++;
        }
        return $index;
    }

    public function jsonSerialize() {
        return [
            'port'=>'port-' . strtolower( $this->port ),
            'properties'=>$this->properties
        ];
    }
}