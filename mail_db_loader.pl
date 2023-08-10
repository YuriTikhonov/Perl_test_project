#!/C:/Strawberryperly/bin/perl
use strict;
use warnings FATAL => 'all';
use DBI;

my @elements;
my $dsn = 'DBI:mysql:mail_db:localhost';
my $db_user_name = 'root';
my $db_password = "password";
my $dbh = DBI -> connect ($dsn, $db_user_name, $db_password) or die "error can\'t connect to DB";
my $my_query = 'INSERT INTO message (created, id, int_id, str) VALUES (?,?,?,?)';
my $log_query = 'INSERT INTO log (created, int_id, str,address) VALUES (?,?,?,?)';
my $sth = $dbh -> prepare ($my_query);
my $sth_log = $dbh -> prepare ($log_query);
my $number = 0;

open FILE, "< maillog" or die "Can't open file: $!";
while (<FILE>) {
    if ($_ =~ /<=/ && $_ =~ /id=/) {
        my $str_val = $_;
        @elements = split(' ',$str_val);
        my $time_stamp = $elements[0] . ' ' . $elements[1];
        my $id_insert;
        my $str_insert;
        for($number = 0;$number <= $#elements;$number++)
        {
            if($elements[$number] =~ /id=/){
                $id_insert = $elements[$number];
            }
            if($number > 1)
            {
                $str_insert .= $elements[$number] .' ';
            }
        }
        $sth -> execute($time_stamp,$id_insert, $elements[2], $str_insert);
    }
    if($_ !~ /<=/ || $_ !~ /id=/){
        my $str_val = $_;
        @elements = split(' ',$str_val);
        my $time_stamp = $elements[0] . ' ' . $elements[1];
         my $address_insert = $elements[4] if (defined($elements[4])) && ($elements[4] =~ /@/);
        my $str_insert;
        for($number = 0;$number <= $#elements;$number++)
        {
            if($number > 1)
            {
                $str_insert .= $elements[$number] .' ';
            }
        }
        $sth_log -> execute($time_stamp, $elements[2], $str_insert,$address_insert);
    }
}
close FILE;






