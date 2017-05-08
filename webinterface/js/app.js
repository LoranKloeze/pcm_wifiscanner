/*
 * PCM Wifiscanner
 * 
 * Copyright 2017 Loran Kloeze - loran@ralon.nl
 * Licentie: MIT
*/

$(function () {
    
    var keep_up_to_date = true;
    
    var updateSsids = function() {
        $.get('/api.php?act=ssids', function (d) {
            var $tbody = $('#mobile_stations tbody');
            $tbody.find('.ssids ul').html('');
            $.each(d, function () {
                var $tr = $('#ms'+this.mobile_station_id);
                if ($tr.length === 1) {
                    var $ul_ssids = $tr.find('.ssids ul');
                    $ul_ssids.append('<li>' + this.ssid + '</li>');
                }

            });
        
        
        });
    }
    
    var updateTable = function () {
        if (keep_up_to_date === false)
            return;
        $.get('/api.php?act=mobile_stations', function (d) {
            var $tbody = $('#mobile_stations tbody');
            $tbody.find('.updated').removeClass('updated');
            $.each(d, function () {
                var $tr = $('#ms'+this.mobile_station_id);
                if ($tr.length === 1) {
                    var $td_last_seen = $tr.find('.last_seen');
                    $td_last_seen.text(this.max_last_seen_on);
                    if ($td_last_seen.attr('data-ts') !== this.max_last_seen_on_ts) {
                        $tr.find('td').addClass('updated');
                        $td_last_seen.attr('data-ts', this.max_last_seen_on_ts);
                        $tr.parent().prepend($tr);
                    }
                } else {
                    $tr = $('<tr>').attr('id', 'ms' + this.mobile_station_id);
                    var $td_mac = $('<td>').addClass('mac').text(this.mac);
                    var $td_ssids = $('<td>').addClass('ssids').append('<ul class="list-unstyled"></ul>');
                    var $td_last_seen = $('<td>').addClass('last_seen').attr('data-ts', this.max_last_seen_on_ts).text(this.max_last_seen_on);
                    $tr.append($td_mac).append($td_ssids).append($td_last_seen);
                    $tr.find('td').addClass('updated');
                    $tbody.prepend($tr);
                }

            });
            updateSsids();
        });
    };
    
    $('#btn-pause').click(function(){
        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).text('Updaten uitzetten');
            keep_up_to_date = true;
            updateTable();
        } else {
            $(this).addClass('active');
            keep_up_to_date = false;     
            $(this).text('Updaten aanzetten');       
        }
            
    });
    
    $('#btn-truncate-db').click(function(){
        keep_up_to_date = false;
        if (window.confirm("De database wordt leeggehaald, weet je dit zeker?")) {
            $.post('/api.php?act=truncate_db', function(){
                $('#mobile_stations tbody').html('');
                keep_up_to_date = true;
            });
        }
        keep_up_to_date = true;
        
    });

    window.setInterval(updateTable, 5000);
    updateTable();

});
