<?php
/**
 * Splatoon MagicWords module for the StrategyWiki extension
 *
 * @file
 * @ingroup Extensions
 * @author Prod (http://www.strategywiki.org/wiki/User:Prod)
 * @author GuyPerfect ()
 * @author Shahar ()
 */

// not a valid entry point
if( !defined( 'MEDIAWIKI' ) ) {
	echo <<<EOT
To install StrategyWiki extension, put the following line in LocalSettings.php:
require_once( "\$IP/extensions/StrategyWiki/StrategyWiki.php" );
EOT;
	exit( 1 );
}

class StrategyWikiSplatoonRotation {
	public static function onParserFirstCallInit( &$parser ) {
		global $wgSplatoonWikiMagicWords;
		if( $wgSplatoonWikiMagicWords ) {
//			$parser->setHook( 'inkrotation',     [ self::class, 'INKRotationRender' ] );
			$parser->setHook( 'splatoon2battle', [ self::class, 'INK2BattleRender' ] );
			$parser->setHook( 'splatoon2shop',   [ self::class, 'INK2ShopRender' ] );
			$parser->setHook( 'splatoon2salmon', [ self::class, 'INK2SalmonRender' ] );
			$parser->setHook( 'splatoon3battle', [ self::class, 'INK3BattleRender' ] );
			$parser->setHook( 'splatoon3shop',   [ self::class, 'INK3ShopRender' ] );
			$parser->setHook( 'splatoon3salmon', [ self::class, 'INK3SalmonRender' ] );
		}
		return true;
	}

	public static function INK2SalmonRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup_schedules = self::fetch2( 'coop_schedules' );
		$markup_results = self::fetch2( 'coop_results' );

		if ( $markup_schedules == null || $markup_results == null ) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone("UTC") );
		$now = $now->format( "M d H:i" );

		$schedule = json_decode( $markup_schedules );
		$result = json_decode( $markup_results );
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{Schedule/Salmon\n";

		for ( $i = 0; $i < 2; $i++ ) {
			$outputPreparse .= self::addSalmon2( $schedule->details[$i] );
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

		$now = new DateTime( "now", new DateTimeZone("UTC") );
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
			$outputPreparse .= self::addSalmon3( $schedule->data->coopGroupingSchedule->regularSchedules->nodes[$i] );

		$outputPreparse .= "|" . $result->data->coopResult->monthlyGear->name;
		$outputPreparse .= "|" . $KINDS[$result->data->coopResult->monthlyGear->__typename];
		$outputPreparse .= "\n";

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK2ShopRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch2('onlineshop/merchandises');
		if ($markup == null) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$KINDS = [
			'clothes' => 'Clothing',
			'head'    => 'Headgear',
			'shoes'   => 'Shoes'
		];

		$now = new DateTime( "now", new DateTimeZone("UTC") );
		$now = $now->format( "M d H:i" );

		$shop = json_decode($markup);
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{Schedule/Shop\n";

		for ($i = 0; $i < 6; $i++) {
			$outputPreparse .= self::addGear2( $shop->merchandises[$i], $KINDS[$shop->merchandises[$i]->gear->kind] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK3ShopRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch3('gear');
		if ($markup == null) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$KINDS = [
			'ClothingGear' => 'Clothing',
			'HeadGear'     => 'Headgear',
			'ShoesGear'    => 'Shoes'
		];

		$now = new DateTime( "now", new DateTimeZone("UTC") );
		$now = $now->format( "M d H:i" );

		$shop = json_decode($markup);
		// Processes markup to extract the merchandise information
		$outputPreparse  = "{{S3Schedule/Shop\n";

		$outputPreparse .= "|" . $shop->data->gesotown->pickupBrand->brand->name;

		//Daily drop gear
		for ($i = 0; $i < 3; $i++) {
			$outputPreparse .= self::addGear3Branded( $shop->data->gesotown->pickupBrand->brandGears[$i], $KINDS[$shop->data->gesotown->pickupBrand->brandGears[$i]->gear->__typename] );
		}
		//nextbrand
		$outputPreparse .= "|" . $shop->data->gesotown->pickupBrand->nextBrand->name;

		//On sale gear
		for ($i = 0; $i < 6; $i++) {
			$outputPreparse .= self::addGear3( $shop->data->gesotown->limitedGears[$i], $KINDS[$shop->data->gesotown->limitedGears[$i]->gear->__typename] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK2BattleRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch2('schedules');
		if ($markup == null) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone("UTC") );
		$now = $now->format( "M d H:i" );

		$schedules = json_decode($markup);
		// Processes markup to extract the schedule information
		// Now
		$outputPreparse  = "{{Schedule/Battle\n";

		for ($i = 0; $i < 2; $i++) {
			$outputPreparse .= self::addMap2( $schedules->regular[$i] );
			$outputPreparse .= self::addMap2( $schedules->gachi[$i] );
			$outputPreparse .= self::addMap2( $schedules->league[$i] );
		}

		$outputPreparse .= "|" . $now . "\n";
		$outputPreparse .= "}}\n";

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INK3BattleRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		$markup = self::fetch3('schedules');
		if ($markup == null) {
			return array( "Could not fetch schedule data from SplatNet." );
		}

		$now = new DateTime( "now", new DateTimeZone("UTC") );
		$now = $now->format( "M d H:i" );

		$schedules = json_decode($markup);
		// Processes markup to extract the schedule information

		if ($schedules->data->regularSchedules->nodes[0]->regularMatchSetting !== null and $schedules->data->regularSchedules->nodes[1]->regularMatchSetting !== null ){
			$outputPreparse  = "{{S3Schedule/Battle\n";

			for ($i = 0; $i < 2; $i++) {
				//Regular Battle
				$outputPreparse .= "|" . $schedules->data->regularSchedules->nodes[$i]->regularMatchSetting->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->regularSchedules->nodes[$i]->regularMatchSetting->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->regularSchedules->nodes[$i]->regularMatchSetting->vsStages[1]->name . "\n";

				//Anarchy
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[0]->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[0]->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[0]->vsStages[1]->name . "\n";
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[1]->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[1]->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->bankaraSchedules->nodes[$i]->bankaraMatchSettings[1]->vsStages[1]->name . "\n";

				//X Battle
				$outputPreparse .= "|" . $schedules->data->xSchedules->nodes[$i]->xMatchSetting->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->xSchedules->nodes[$i]->xMatchSetting->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->xSchedules->nodes[$i]->xMatchSetting->vsStages[1]->name . "\n";

				//League Battle
				$outputPreparse .= "|" . $schedules->data->leagueSchedules->nodes[$i]->leagueMatchSetting->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->leagueSchedules->nodes[$i]->leagueMatchSetting->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->leagueSchedules->nodes[$i]->leagueMatchSetting->vsStages[1]->name . "\n";
			}

			$outputPreparse .= "|" . $now . "\n";
			$outputPreparse .= "}}\n";
		}

		if ($schedules->data->festSchedules->nodes[0]->festMatchSetting !== null and $schedules->data->festSchedules->nodes[1]->festMatchSetting !== null ){
			$outputPreparse  = "{{S3Schedule/BattleFest\n";

			for ($i = 0; $i < 2; $i++) {
				//Splatfest
				$outputPreparse .= "|" . $schedules->data->festSchedules->nodes[$i]->festMatchSetting->vsRule->name;
				$outputPreparse .= "|" . $schedules->data->festSchedules->nodes[$i]->festMatchSetting->vsStages[0]->name;
				$outputPreparse .= "|" . $schedules->data->festSchedules->nodes[$i]->festMatchSetting->vsStages[1]->name . "\n";
			}

			$outputPreparse .= "|" . $schedules->data->currentFest->tricolorStage->name . "\n";

			$outputPreparse .= "|" . $now . "\n";
			$outputPreparse .= "}}\n";
		}

		return array( $parser->recursiveTagParse( $outputPreparse, $frame ) );
	}

	public static function INKRotationRender( $input, array $args, Parser $parser, PPFrame $frame ) {
		global $wgSplatoonWikiRotationCookie;

		// Retrieve the schedule markup from SplatNet
		$markup = self::fetch1($wgSplatoonWikiRotationCookie);
		if ($markup == null) {
			return array( "Could not fetch schedule markup from SplatNet." );
		}

//		<countdown time="12/31/2015 5:00 AM UTC"><H>:<M>:<S></countdown>
		$now = new DateTime();
		$now->setTime(floor((date('H') - 2)/4) * 4 + 2, 0);

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
		$outputPreparse .= "In <countdown time=\"" . $now->add(new DateInterval('PT4H'))->format('n/j/Y g:00 A') . " UTC\"><H>:<M>:<S></countdown>\n\n";
		$outputPreparse .= "[[File:Symbol TWF.svg|link=Regular Battle|25px]] <span style=\"font-size: 16px;\">'''Regular Battle - [[Turf War]]'''</span>\n";

		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n\n";
		$outputPreparse .= self::addRankedRule( $markup );
		$outputPreparse .= self::addMaps( $markup );
		$outputPreparse .= "\n";

		$outputPreparse .= "<noinclude>";

		//Later
		$outputPreparse .= "| class=\"textwidget\" style=\"width:30%; padding:2%\" |<big><big><big>'''Later Stages'''</big></big></big>\n";
		$outputPreparse .= "In <countdown time=\"" . $now->add(new DateInterval('PT4H'))->format('n/j/Y g:00 A') . " UTC\"><H>:<M>:<S></countdown>\n\n";
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
		$output  = "|" . trim($map->rule->name);
		$output .= "|" . trim($map->stage_a->name);
		$output .= "|" . trim($map->stage_b->name);
		$output .= "\n";

		return $output;
	}

	private static function addGear2( $gear, $type ) {
		return "|" . $type . "|" . rtrim($gear->gear->name) . "|" . number_format( $gear->price ) . "|" . $gear->skill->name . "|" . $gear->gear->brand->name . "\n";
	}

	private static function addGear3( $gear, $type ) {
		return "|" . $type . "|" . rtrim($gear->gear->name) . "|" . number_format( $gear->price ) . "|" . $gear->gear->primaryGearPower->name . "|" . $gear->gear->brand->name . "\n";
	}

	private static function addGear3Branded( $gear, $type ) {
		return "|" . $type . "|" . rtrim($gear->gear->name) . "|" . number_format( $gear->price ) . "|" . $gear->gear->primaryGearPower->name . "\n";
	}

	private static function addSalmon2( $salmon ) {
		$output  = "|" . self::formatTime( $salmon->start_time );
		$output .= "|" . self::formatTime( $salmon->end_time );
		$output .= "|" . rtrim($salmon->stage->name);
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

		$output .= "\n";

		return $output;
	}

	private static function formatTime($timestamp) {
		$time = new DateTime("now", new DateTimeZone("UTC"));

		return $time->setTimestamp((int) $timestamp)->format("M d H:i");
	}

	private static function salmonWeapon( $weapon ){
		return ($weapon->id == -1) ? "?" : (($weapon->id == -2) ? "??" : trim($weapon->weapon->name));
	}

	private static function salmon3Weapon( $weapon ){
		return ($weapon->__splatoon3ink_id == "edcfecb7e8acd1a7") ? "??" : (($weapon->name == "Random") ? "?" : trim($weapon->name));
	}

	private static function addRankedRule( &$markup ) {
		$ruleName = self::getValueById( $markup, 'rule-description' );
		return "[[File:Symbol RankedF.svg|link=Ranked Battle|25px]] <span style=\"font-size: 16px;\">'''Ranked Battle - [[File:Mode Icon " . $ruleName . ".png|link=" . $ruleName . "|25px]] [[" . $ruleName . "]]'''</span>\n";
	}

	// Download schedule markup from SplatFest
	private static function fetch1($cookie) {
		$c = curl_init('https://splatoon.nintendo.net/schedule?locale=en');
		curl_setopt($c, CURLOPT_COOKIE, '_wag_session=' . $cookie);
		curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
		$ret = curl_exec($c);
		curl_close($c);
		return $ret ? $ret : null;
	}

	// Download schedule markup from SplatFest
	private static function fetch2($url) {
		global $wgSplatoonWikiRotation2Cookie;

		$c = curl_init('https://app.splatoon2.nintendo.net/api/' . $url);
		curl_setopt($c, CURLOPT_COOKIE, 'iksm_session=' . $wgSplatoonWikiRotation2Cookie);
		curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
		$ret = curl_exec($c);
		curl_close($c);
		return $ret ? $ret : null;
	}

	public static function fetch3($url) {
		global $wgSplatoonWikiRotation2Cookie;

		$c = curl_init('https://splatoon3.ink/data/' . $url . '.json');
		curl_setopt($c, CURLOPT_RETURNTRANSFER, 1);
		$ret = curl_exec($c);
		curl_close($c);
		return $ret ? $ret : null;
    }

	// Finds an element descriptor in the markup and parses out its content
	private static function getValueById(&$markup, $descriptor) {
		$x	    = strpos($markup, '>', strpos($markup, $descriptor)) + 1;
		$y	    = strpos($markup, '<', $x);
		$ret	= str_replace('&#39;', '\'', substr($markup, $x, $y - $x));
		$markup = substr($markup, $y);
		return $ret;
	}
}
