import React from 'react';
import { Link } from 'react-router';
import { connect } from 'react-redux';
// import baseStyles from './DemoApp.less';

const Header = (props) => {
  const { translate } = props;
  return (
    <div className='header'}>
      <div className='headerContent'}>
        <h1>{translate('_title_nucleus__resx')}</h1>
        <ul className={baseStyles.util}>
          <li>
            <a href = "//wiki/pages/viewpage.action?pageId=34295371" target="_blank">
              {translate('_link_wiki__resx')}
            </a>
          </li>
          <li>
            <Link to = "/">{translate('_link_home__resx')}</Link>
          </li>
        </ul>
      </div>
    </div>
    );
};

Header.displayName = 'Header';

Header.propTypes = {
  translate: React.PropTypes.func
};

export default Header;
