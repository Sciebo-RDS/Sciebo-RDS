<?php
namespace OCA\RDS\Db;

use JsonSerializable;

use OCP\AppFramework\Db\Entity;

class Port extends Entity implements JsonSerializable {

    protected $port;
    protected $properties;

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

    public function propertiesEqual( $port ) {
        foreach ( $port->properties as $prop ) {
            $index = $this->getIndexOfProperty( $port->properties );

            if ( $index == NULL || $this->properties[$index]['value'] != $value ) {
                return FALSE;
            }
        }

        return TRUE;
    }

    public function notEqualPropertyIndices( $port ) {
        $returnList = [];

        foreach ( $port->properties as $prop ) {
            $index = $this->getIndexOfProperty( $port->properties );

            if ( $index == NULL || $this->properties[$index]['value'] != $value ) {
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
            'id'=>$this->id,
            'port'=>$this->port,
            'properties'=>$this->properties
        ];
    }
}