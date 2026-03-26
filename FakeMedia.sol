pragma solidity >= 0.8.11 <= 0.8.11;

contract FakeMedia {
    string public users;
    string public news;
       
    //add user details who are registered to access IOT and user password will be encrypted with sha512	
    function addUser(string memory us) public {
       users = us;	
    }
   //get user details
    function getUser() public view returns (string memory) {
        return users;
    }

    function setNews(string memory n) public {
       news= n;	
    }

    function getNews() public view returns (string memory) {
        return news;
    }

    constructor() public {
        users = "";
	news="";
    }
}