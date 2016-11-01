var app = angular.module('giphytags',[]);

app.controller('sentimentController', function($scope, $http, $anchorScroll) {

    /**
     * handle of twitter user being examined
     * @type {string}
     */
    $scope.uid = '';

    /**
     * candidates (name,twitter) mapped by role
     * @type {{}}
     */
    $scope.races = {};

    /**
     * initial setup
     */
    $scope.init = function() {
        resetScope(false);
        $scope.getRaces();
    };

    /**
     * reset state before (re)loading sentiment data
     * @param waiting show waiting spinner?
     */
    var resetScope = function(waiting) {
        $scope.error = null;
        $scope.waitingUser = waiting;
        $scope.waitingMentions = waiting;
        $scope.resultUser = null;
        $scope.resultMentions = null;
    };

    /**
     * load candidates (static file for now)
     */
    $scope.getRaces = function() {
        $http({method:'GET',url:'/static/races.json'}).then(
            function(response) {
                if(response.data.error) {
                    $scope.error = response.data.error;
                } else {
                    $scope.races = response.data;
                }
            },
            function(response) {
                $scope.error = response.statusText;
            }
        )
    };

    /**
     * retrieve sentiment analysis of tweets by, and tweets about, a twitter user
     * @param uid twitter handle to examine
     */
    $scope.analyzePolitician = function(uid) {
        if($scope.waitingUser||$scope.waitingMentions) {
            return alert('Please wait until the current data has finished loading');
        }
        if(uid) {
            $scope.uid=uid.indexOf('@')==0?uid:'@'+uid;
        }
        resetScope(true);
        $anchorScroll('results');
        $http({method:'POST',url:'/json/analyze_user',data:{uid:$scope.uid}}).then(
            function(response) {
                if(response.data.error) {
                    $scope.error = response.data.error;
                } else {
                    $scope.resultUser = response.data;
                }
            },
            function(response) {
                $scope.error = response.statusText;
            }
        ).finally(function() {$scope.waitingUser = false;});
        $http({method:'POST',url:'/json/analyze_mentions',data:{uid:$scope.uid}}).then(
            function(response) {
                if(response.data.error) {
                    $scope.error = response.data.error;
                } else {
                    $scope.resultMentions = response.data;
                }
            },
            function(response) {
                $scope.error = response.statusText;
            }
        ).finally(function() {$scope.waitingMentions = false;});
    };

    /**
     * open a new window to search twitter for the given keyword
     * @param keyword
     */
    $scope.linkKeyword = function(keyword) {
        window.open('http://twitter.com/search?q='+keyword,'_blank');
    };

    /**
     * open a new window to display the selected tweet
     * @param tweet
     */
    $scope.linkTweet = function(tweet) {
        window.open(tweet.tweet_url,'_blank');
    };

    /**
     * does the provided array contain the needle?
     * @param needle
     * @param array
     * @returns {boolean}
     */
    $scope.contains = function (needle, array) {
        return array?array.indexOf(needle)>=0:false;
    };

});