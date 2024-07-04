<?php
/**
 * Splatoon MagicWords module for the StrategyWiki extension
 *
 * @file
 * @ingroup Extensions
 * @author Prod (http://www.strategywiki.org/wiki/User:Prod)
 * @author GuyPerfect ()
 * @author Shahar ()
 * @author Inkrid ()
 */

namespace MediaWiki\Extension\StrategyWiki;

use Config;
use DateTime;
use DateTimeZone;
use MediaWiki\Hook\ParserFirstCallInitHook;
use Parser;
use PPFrame;

class SplatoonRotationHooks implements ParserFirstCallInitHook {
	private $config;

	/**
	 * @param Config $config
	 */
	public function __construct( Config $config ) {
		$this->config = $config;
	}

	public function onParserFirstCallInit( $parser ) {
		if ( $this->config->get( 'SplatoonWikiMagicWords' ) ) {
//			$parser->setHook( 'inkrotation',     [ self::class, 'INKRotationRender' ] );
			$parser->setHook( 'splatoon2battle', [ self::class, 'INK2BattleRender' ] );
			$parser->setHook( 'splatoon2shop',   [ self::class, 'INK2ShopRender' ] );
			$parser->setHook( 'splatoon2salmon', [ self::class, 'INK2SalmonRender' ] );
			$parser->setHook( 'splatoon3battle', [ self::class, 'INK3BattleRender' ] );
			$parser->setHook( 'splatoon3shop',   [ self::class, 'INK3ShopRender' ] );
			$parser->setHook( 'splatoon3salmon', [ self::class, 'INK3SalmonRender' ] );
		}
	}

	public static function INK2SalmonRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup_schedules = self::fetch2( 'coop_schedules' );
		$markup_results = self::fetch2( 'coop_results' );

		if ( $markup_schedules == null || $markup_results == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$schedule = json_decode( $markup_schedules );
		$result = json_decode( $markup_results );
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{Schedule/Salmon\n";

		for ( $i = 0; $i < 2; $i++ ) {
			$outputPreparse .= self::addSalmon2( $schedule->details[ $i ] );
		}

		$outputPreparse .= "|" . $result->reward_gear->name;
		$outputPreparse .= "|" . $result->reward_gear->kind;
		$outputPreparse .= "\n";

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK3SalmonRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup_schedules = self::fetch3( 'schedules' );
		$markup_results = self::fetch3( 'coop' );

		if ( $markup_schedules == null || $markup_results == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$schedule = json_decode( $markup_schedules );
		$result = json_decode( $markup_results );
		// Processes markup to extract the salmon run information
		$outputPreparse  = "{{S3Schedule/Salmon\n";

		$KINDS = [
			'ClothingGear' => 'Clothing',
			'HeadGear'     => 'Headgear',
			'ShoesGear'    => 'Shoes'
		];

		for ( $i = 0; $i < 2; $i++ )
			$outputPreparse .= self::addSalmon3( $schedule->data->coopGroupingSchedule->regularSchedules->nodes[ $i ] );

		$outputPreparse .= "|" . $result->data->coopResult->monthlyGear->name;
		$outputPreparse .= "|" . $KINDS[ $result->data->coopResult->monthlyGear->__typename ];
		$outputPreparse .= "\n";

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK2ShopRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch2( 'onlineshop/merchandises' );
		if ( $markup == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$KINDS = [
			'clothes' => 'Clothing',
			'head'    => 'Headgear',
			'shoes'   => 'Shoes'
		];

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$shop = json_decode( $markup );
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{Schedule/Shop\n";

		for ( $i = 0; $i < 6; $i++ ) {
			$outputPreparse .= self::addGear2( $shop->merchandises[ $i ], $KINDS[ $shop->merchandises[ $i ]->gear->kind ] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK3ShopRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch3( 'gear' );
		if ( $markup == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$KINDS = [
			'ClothingGear' => 'Clothing',
			'HeadGear'     => 'Headgear',
			'ShoesGear'    => 'Shoes'
		];

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$shop = json_decode( $markup );
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{S3Schedule/Shop\n";

		$outputPreparse .= "|" . $shop->data->gesotown->pickupBrand->brand->name;

		//Daily drop gear
		for ( $i = 0; $i < 3; $i++ ) {
			$outputPreparse .= self::addGear3Branded( $shop->data->gesotown->pickupBrand->brandGears[ $i ], $KINDS[ $shop->data->gesotown->pickupBrand->brandGears[ $i ]->gear->__typename ] );
		}
		//nextbrand
		$outputPreparse .= "|" . $shop->data->gesotown->pickupBrand->nextBrand->name;

		//On sale gear
		for ( $i = 0; $i < 6; $i++ ) {
			$outputPreparse .= self::addGear3( $shop->data->gesotown->limitedGears[ $i ], $KINDS[ $shop->data->gesotown->limitedGears[ $i ]->gear->__typename ] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK2BattleRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch2( 'schedules' );
		if ( $markup == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$schedules = json_decode( $markup );
		// Processes markup to extract the schedule information
		// Now
		$outputPreparse  = "{{Schedule/Battle\n";

		for ( $i = 0; $i < 2; $i++ ) {
			$outputPreparse .= self::addMap2( $schedules->regular[ $i ] );
			$outputPreparse .= self::addMap2( $schedules->gachi[ $i ] );
			$outputPreparse .= self::addMap2( $schedules->league[ $i ] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK3BattleRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch3( 'schedules' );
		if ( $markup == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone( "UTC" ) );
		$now = $now->format( "M d H:i" );

		$schedules = json_decode( $markup );
		// Processes markup to extract the schedule information

		$hasRegular = $schedules->data->regularSchedules->nodes[ 0 ]->regularMatchSetting !== null || $schedules->data->regularSchedules->nodes[ 1 ]->regularMatchSetting !== null;
		$hasFest = ( $schedules->data->festSchedules->nodes[ 0 ]->festMatchSettings !== null ) || ( $schedules->data->festSchedules->nodes[ 1 ]->festMatchSettings !== null );
		$hasAny = $hasRegular || $hasFest;

		if ( $hasAny ){
			$outputPreparse  = "{{S3Schedule/Battle\n";
		}

		if ( $hasRegular ){
			for ( $i = 0; $i < 2; $i++ ) {
				//Regular Battle
				$outputPreparse .= "|regmode_"   . strval( $i ) . "=" . $schedules->data->regularSchedules->nodes[ $i ]->regularMatchSetting->vsRule->name;
				$outputPreparse .= "|regstage1_" . strval( $i ) . "=" . $schedules->data->regularSchedules->nodes[ $i ]->regularMatchSetting->vsStages[ 0 ]->name;
				$outputPreparse .= "|regstage2_" . strval( $i ) . "=" . $schedules->data->regularSchedules->nodes[ $i ]->regularMatchSetting->vsStages[ 1 ]->name . "\n";

				//Anarchy
				$outputPreparse .= "|anaseriesmode_"   . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 0 ]->vsRule->name;
				$outputPreparse .= "|anaseriesstage1_" . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 0 ]->vsStages[ 0 ]->name;
				$outputPreparse .= "|anaseriesstage2_" . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 0 ]->vsStages[ 1 ]->name . "\n";
				$outputPreparse .= "|anaopenmode_"	   . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 1 ]->vsRule->name;
				$outputPreparse .= "|anaopenstage1_"   . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 1 ]->vsStages[ 0 ]->name;
				$outputPreparse .= "|anaopenstage2_"   . strval( $i ) . "=" . $schedules->data->bankaraSchedules->nodes[ $i ]->bankaraMatchSettings[ 1 ]->vsStages[ 1 ]->name . "\n";

				//X Battle
				$outputPreparse .= "|xmode_"   . strval( $i ) . "=" . $schedules->data->xSchedules->nodes[ $i ]->xMatchSetting->vsRule->name;
				$outputPreparse .= "|xstage1_" . strval( $i ) . "=" . $schedules->data->xSchedules->nodes[ $i ]->xMatchSetting->vsStages[ 0 ]->name;
				$outputPreparse .= "|xstage2_" . strval( $i ) . "=" . $schedules->data->xSchedules->nodes[ $i ]->xMatchSetting->vsStages[ 1 ]->name . "\n";

				//League Battle
				$outputPreparse .= "|leaguemode_"   . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[ $i ]->leagueMatchSetting->vsRule->name;
				$outputPreparse .= "|leaguestage1_" . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[ $i ]->leagueMatchSetting->vsStages[ 0 ]->name;
				$outputPreparse .= "|leaguestage2_" . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[ $i ]->leagueMatchSetting->vsStages[ 1 ]->name . "\n";
				$outputPreparse .= "|leaguename_"   . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[ $i ]->leagueMatchSetting->leagueMatchEvent->name . "\n";
				$outputPreparse .= "|leaguedesc_"   . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[ $i ]->leagueMatchSetting->leagueMatchEvent->desc . "\n";
				$outputPreparse .= "|leagueregulation_" . strval( $i ) . "=" . $schedules->data->eventSchedules->nodes[$i]->leagueMatchSetting->leagueMatchEvent->regulation . "\n";
				for ( $j = 0; $j < 6; $j++ ) {
					if ( isset( $schedules->data->eventSchedules->nodes[ $i ]->timePeriods[ $j ] ) ){
						$outputPreparse .= "|leaguestarttime" . strval( $j + 1 ) . "_" . strval( $i ) . "=" . self::formatTime( strtotime( $schedules->data->eventSchedules->nodes[ $i ]->timePeriods[ $j ]->startTime ) ) . "\n";
						$outputPreparse .= "|leagueendtime" . strval( $j + 1 ) . "_"   . strval( $i ) . "=" . self::formatTime( strtotime( $schedules->data->eventSchedules->nodes[ $i ]->timePeriods[ $j ]->endTime ) ) . "\n";
					} else {
						$outputPreparse .= "|leaguestarttime" . strval( $j + 1 ) . "_" . strval( $i ) . "=Jan 01 00:00\n";
						$outputPreparse .= "|leagueendtime" . strval( $j + 1 ) . "_"   . strval( $i ) . "=Jan 01 00:00\n";
					}
				}
			}

		}

		if ( $hasFest ){
			for ( $i = 0; $i < 2; $i++ ) {
				//Splatfest
				$outputPreparse .= "|festpromode_"    . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 0 ]->vsRule->name;
				$outputPreparse .= "|festprostage1_"  . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 0 ]->vsStages[ 0 ]->name;
				$outputPreparse .= "|festprostage2_"  . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 0 ]->vsStages[ 1 ]->name . "\n";
				$outputPreparse .= "|festopenmode_"   . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 1 ]->vsRule->name;
				$outputPreparse .= "|festopenstage1_" . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 1 ]->vsStages[ 0 ]->name;
				$outputPreparse .= "|festopenstage2_" . strval( $i ) . "=" . $schedules->data->festSchedules->nodes[ $i ]->festMatchSettings[ 1 ]->vsStages[ 1 ]->name . "\n";
			}

			$outputPreparse .= "|tricolorstage=" . $schedules->data->currentFest->tricolorStage->name . "\n";
		}

		if ( $hasAny ){
			$outputPreparse .= "|time=" . $now . "\n";
			$outputPreparse .= "}}\n";
		}

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INKRotationRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		global $wgSplatoonWikiRotationCookie;

		// Retrieve the schedule markup from SplatNet
		$markup = self::fetch1( $wgSplatoonWikiRotationCookie );
		if ( $markup == null ) {
			return array( "Could not fetch schedule markup from SplatNet." );
		}

//		<countdown time="12/31/2015 5:00 AM UTC"><H>:<M>:<S></countdown>
		$now = new DateTime();
		$now->setTime( floor( ( date( 'H' ) - 2 )/4 ) * 4 + 2, 0 );

		// Processes markup to extract the schedule information
		// Now
		$outputPreparse  = "{| style=\"width:100%\"\n";
		$outputPreparse .= "| class=\"textwidget\" style=\"width:30%; padding:2%\" |<big><big><big>'''Current Stages'''</big></big></big>\n";
		$outputPreparse .= "<br />\n\n";
		$outputPreparse .= "[[File:Symbol TWF.svg|link=Regular Battle|25px]] <span style=\"font-size: 16px;\">'''Regular Battle - [[Turf War]]'''</span>\n";

		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n\n";
		$outputPreparse .= self::addRankedRule( $markup );
		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n";

		//Next
		$outputPreparse .= "| class=\"textwidget\" style=\"width:30%; padding:2%\" |<big><big><big>'''Next Stages'''</big></big></big>\n";
		$outputPreparse .= "In <countdown time=\"" . $now->add( new DateInterval( 'PT4H' ) )->format( 'n/j/Y g:00 A' ) . " UTC\"><H>:<M>:<S></countdown>\n\n";
		$outputPreparse .= "[[File:Symbol TWF.svg|link=Regular Battle|25px]] <span style=\"font-size: 16px;\">'''Regular Battle - [[Turf War]]'''</span>\n";

		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n\n";
		$outputPreparse .= self::addRankedRule( $markup );
		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n";

		$outputPreparse .= "<noinclude>";

		//Later
		$outputPreparse .= "| class=\"textwidget\" style=\"width:30%; padding:2%\" |<big><big><big>'''Later Stages'''</big></big></big>\n";
		$outputPreparse .= "In <countdown time=\"" . $now->add( new DateInterval( 'PT4H' ) )->format( 'n/j/Y g:00 A' ) . " UTC\"><H>:<M>:<S></countdown>\n\n";
		$outputPreparse .= "[[File:Symbol TWF.svg|link=Regular Battle|25px]] <span style=\"font-size: 16px;\">'''Regular Battle - [[Turf War]]'''</span>\n";

		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n\n";
		$outputPreparse .= self::addRankedRule( $markup );
		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n";

		$outputPreparse .= "</noinclude>";

		$outputPreparse .= "|}\n";

		$outputPreparse .= "<p class=\"textwidget\"><span style=\"font-size: 10px;\">Last fetched: " . wfTimestamp( TS_RFC2822 ) . "</span></p>\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	private static function addMaps( &$markup ) {
		$output  = "<table style=\"margin-left: auto; margin-right: auto\"><tr>";
		$output .= self::addMap( $markup );
		$output .= self::addMap( $markup );
		$output .= "</tr></table>";

		return $output;
	}

	private static function addMap( &$markup ) {
		$mapName = self::getValueById( $markup, 'map-name' );
		return "<td style=\"vertical-align: top; width: 60px\">[[File:Splatoon Stage " . $mapName . ".png|x60px|link=" . $mapName . "|" . $mapName . "]]<br />[[" . $mapName . "]]</td>";
	}

	private static function addMap2( $map ) {
		$output  = "|" . trim( $map->rule->name );
		$output .= "|" . trim( $map->stage_a->name );
		$output .= "|" . trim( $map->stage_b->name );
		$output .= "\n";

		return $output;
	}

	private static function addGear2( $gear, $type ) {
		return "|" . $type . "|" . rtrim( $gear->gear->name ) . "|" . number_format( $gear->price ) . "|" . $gear->skill->name . "|" . $gear->gear->brand->name . "\n";
	}

	private static function addGear3( $gear, $type ) {
		return "|" . $type . "|" . rtrim( $gear->gear->name ) . "|" . number_format( $gear->price ) . "|" . $gear->gear->primaryGearPower->name . "|" . $gear->gear->brand->name . "\n";
	}

	private static function addGear3Branded( $gear, $type ) {
		return "|" . $type . "|" . rtrim( $gear->gear->name ) . "|" . number_format( $gear->price ) . "|" . $gear->gear->primaryGearPower->name . "\n";
	}

	private static function addSalmon2( $salmon ) {
		$output  = "|" . self::formatTime( $salmon->start_time );
		$output .= "|" . self::formatTime( $salmon->end_time );
		$output .= "|" . rtrim( $salmon->stage->name );
		$output .= "|" . self::salmonWeapon( $salmon->weapons[0] );
		$output .= "|" . self::salmonWeapon( $salmon->weapons[1] );
		$output .= "|" . self::salmonWeapon( $salmon->weapons[2] );
		$output .= "|" . self::salmonWeapon( $salmon->weapons[3] );
		$output .= "\n";

		return $output;
	}

	private static function addSalmon3( $salmon ) {
		$output  = "|" . self::formatTime( strtotime( $salmon->startTime ) );
		$output .= "|" . self::formatTime( strtotime( $salmon->endTime ) );
		$output .= "|" . rtrim( $salmon->setting->coopStage->name );

		for( $i = 0; $i <= 3; $i++ )
			$output .= "|" . self::salmon3Weapon( $salmon->setting->weapons[$i] );

		$output .= "|" . $salmon->__splatoon3ink_king_salmonid_guess . "\n";
		$output .= "\n";

		return $output;
	}

	private static function formatTime( $timestamp ) {
		$time = new DateTime( "now", new DateTimeZone( "UTC" ) );

		return $time->setTimestamp( (int)$timestamp )->format( "M d H:i" );
	}

	private static function salmonWeapon( $weapon ) {
		return ( $weapon->id == -1 ) ? "?" : ( ( $weapon->id == -2 ) ? "??" : trim( $weapon->weapon->name ) );
	}

	private static function salmon3Weapon( $weapon ) {
		return ( $weapon->image->url == "https://splatoon3.ink/assets/splatnet/v2/ui_img/9d7272733ae2f2282938da17d69f13419a935eef42239132a02fcf37d8678f10_0.png" ) ? "??" : ( ( $weapon->name == "Random" ) ? "?" : trim( $weapon->name ) );
	}

	private static function addRankedRule( &$markup ) {
		$ruleName = self::getValueById( $markup, 'rule-description' );
		return "[[File:Symbol RankedF.svg|link=Ranked Battle|25px]] <span style=\"font-size: 16px;\">'''Ranked Battle - [[File:Mode Icon " . $ruleName . ".png|link=" . $ruleName . "|25px]] [[" . $ruleName . "]]'''</span>\n";
	}

	// Download schedule markup from SplatFest
	private static function fetch1( $cookie ) {
		$c = curl_init( 'https://splatoon.nintendo.net/schedule?locale=en' );
		curl_setopt( $c, CURLOPT_COOKIE, '_wag_session=' . $cookie );
		curl_setopt( $c, CURLOPT_RETURNTRANSFER, 1 );
		$ret = curl_exec( $c );
		curl_close( $c );
		return $ret ? $ret : null;
	}

	// Download schedule markup from SplatFest
	private static function fetch2( $url ) {
		global $wgSplatoonWikiRotation2Cookie;

		$c = curl_init( 'https://app.splatoon2.nintendo.net/api/' . $url );
		curl_setopt( $c, CURLOPT_COOKIE, 'iksm_session=' . $wgSplatoonWikiRotation2Cookie );
		curl_setopt( $c, CURLOPT_RETURNTRANSFER, 1 );
		$ret = curl_exec( $c );
		curl_close( $c );
		return $ret ? $ret : null;
	}

	public static function fetch3( $url ) {
		global $wgSplatoonWikiRotation2Cookie;

		$c = curl_init( 'https://splatoon3.ink/data/' . $url . '.json' );
		curl_setopt( $c, CURLOPT_RETURNTRANSFER, 1 );
		$ret = curl_exec( $c );
		curl_close( $c );
		return $ret ? $ret : null;
	}

	// Finds an element descriptor in the markup and parses out its content
	private static function getValueById( &$markup, $descriptor ) {
		$x	    = strpos( $markup, '>', strpos( $markup, $descriptor ) ) + 1;
		$y	    = strpos( $markup, '<', $x );
		$ret	= str_replace( '&#39;', '\'', substr( $markup, $x, $y - $x ) );
		$markup = substr( $markup, $y );
		return $ret;
	}
}
