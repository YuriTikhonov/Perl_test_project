#!C:\Strawberry\perl\bin\perl.exe
use strict;
use warnings FATAL => 'all';
use CGI;
use DBI;

my $cgi = CGI->new;
print $cgi->header(-type => "text/html", -charset => "UTF-8");
mail_search($cgi);

if($cgi->param('address')) {
    display_results($cgi);
}else{
    search_form($cgi);
}

sub mail_search {
  my ($cgi) = @_;
    print $cgi->start_html(
        -title => "Mail Search",
        -style => {
            -src => "style.css"
        }
    );
    print $cgi->h2("Mail Search");
}

sub display_results {
    my ($cgi) = @_;
    my $mail_address = $cgi->param('address');
    $mail_address =~ s/^\s+|\s+$//g;
    my $dsn = 'DBI:mysql:mail_db:localhost';
    my $db_user_name = 'root';
    my $db_password = "password";
    my $dbh = DBI -> connect ($dsn, $db_user_name, $db_password) or die "error can\'t connect to DB";
    my $my_query = "SELECT * FROM(SELECT message.created, message.str, message.int_id FROM  message
        WHERE  message.str LIKE  '%<= $mail_address%'
        UNION
        SELECT log.created,log.str,log.int_id FROM log
        WHERE log.address = '$mail_address')A
       ORDER BY UNIX_TIMESTAMP(created) DESC, int_id LIMIT 100;";
    my $sth = $dbh -> prepare ($my_query);
    $sth -> execute();
    search_form($cgi);
    my $str_count = 0;
    while (my @row = $sth->fetchrow_array()) {
        if($row[1] =~ /$mail_address/ && $str_count < 100){
            $str_count++;
            print $cgi->p("$row[0] $row[1]");
         if($str_count == 100){
             print $cgi->h2("More than 100 results found. Please refine your search");
         }
        }
    }
    $sth->finish();
}

sub search_form {
my ($cgi) = @_;
    print $cgi->start_form(
        -name => 'main',
        -method => 'POST',
    );
    print $cgi->textfield(
        -name => 'address',
        -placeholder => "Enter your mail address"
    );
    print $cgi->submit(
        -name => "submit",
        -value => "Submit"
    );
    print $cgi->end_form;
}



