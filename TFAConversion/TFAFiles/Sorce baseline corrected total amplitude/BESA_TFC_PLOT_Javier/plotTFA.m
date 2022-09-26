% Plot time-frequency charts using data at TFA structure
%
% SYNTAX:
%
% htmf = plotTFA(TFA, datatype, binArray, chanArray, amprange, twindow, fwindow, blcwin, blctype, fshading, fcontour, Ylog, plotype, surfacetype, cbname, cbscale)
%
% OUTPUT
%
% htmf        - returns the handle for an image graphics object. Use h to modify a specific chart lines after it is created.
%
% INPUTS:
%
% TFA         - Time-frequency data structure
% datatype    - Type of data to plot. 0=POWER; 1=PHASE; 2=AMPLITUDE; 3=ITC; 4=Induced Power
% binArray    - bin (indices) to plot. E.g. [ 3 5 7]
% chanArray   - channel (indices) to plot. E.g. [ 10 12 34 65];
%
%               By default the plotting style is "topografic view" (see 'plotype' for "rectangular view").
%               However, if you want to plot specific channels in specific rows then you have to
%               create a cell array containing the channel indices for each row.
%               For example: Create 3 rows of plots. Plot channels 2, 3 and 4 in the first row;
%               channels 23, 24, 25, and 32 in the second row; and finally channels 45 and 46 in the
%               third row. The cell array must be as follows:
%
%                                   {[2 3 4];[23 24 25 32];[ 45 46]}
%
%
%               IMPORTANT: if you enter chanArray as a cell array then 'plotype' option will be
%               ignored.
%
%
% amprange    - amplitude range (Z-scale) (displayed as colormap) to plot. E.g. [-2 2]%
%               Alternatively, if the string 'auto' is entered here, each channel will have its own
%               auto-scale
%
%
% twindow     - time range (X-scale) in ms to plot. E.g. [-200 800]
%               time ticks (XTicks) can be specified as part of this
%               2-value variable by adding a 3rd or more values. For instance [-200 800 100:50:800] means
%               that twindow is [-200 800] and time ticks are [100 150 200 250 ...800]
%
% fwindow     - frequency range (Y-scale) in Hz to plot. E.g. [0.5 55]
%               frequency ticks (YTicks) can be specified as part of this
%               2-value variable by adding a 3rd or more values. For instance [0.5 55 10 20 40 60] means
%               that fwindow is [0.5 55] and frequency ticks are [10 20 40 60]
%
% blcwin      - baseline correction window in ms. E.g. [-100 0]
% blctype     - baseline correction type. Can be 'subtractive', 'divisive', or 'none'
%                * 'subtractive' : gets the mean value within "blcwin" per frequency band,
%                   and then substract that value from each corresponding whole
%                   frequency band.
%                * 'divisive' : gets the mean value within "blcwin" per frequency band,
%                   and then divide each whole frequency band by that value, accordingly.
%                * 'TSE' : gets the mean value within "blcwin" per frequency band,
%                   and then substracts that value from each corresponding 
%                   frequency band, and then divide the subtracted value by the previous 
%                   mean value, accordingly.
%                * 'none' : do not perform baseline correction at all.
%
% fshading    - controls of color shading. Can be 'flat' or  'interp'.
%
% fcontour    - displays isolines calculated from matrix Z and fills the areas between the isolines using
%               constant colors corresponding to the current figure's
%               colormap. Can be 'on' or  'off'.
%
% Ylog        - Logarithmic scale for frequency range (fwindow).
%               Can be 1 (means apply log scale)  or  0 (means apply linear scale)
%
% plotype    - Plotting style: 0 means topographic; 1 means rectangular array.
%               IMPORTANT: if you enter chanArray as a cell array then this 'plotype' option will be
%               ignored.
% surfacetype  - '2D' {default} or '3D'
% cbname       - color bar name. e.g. 'jet'
% cbscale      - % 'linear' {default}, 'dB', 'whitened' 
%
%
%
%
% Author: Javier Lopez-Calderon and Johanna Kreither
% Manhattan, New York
% 2016
%
% ###################################################################################
%
% You'll need the Special Edition of ERPLAB, version 4.0.6.X (private version).
% Contact inheniero@gmail.com to get it.
%
% ###################################################################################
%
% Last update: 09/23/2016. JLC
%         - enter chanArray as cell array
%         - 'plotype' option
%         - automatic X- and Y-axis ticks fixed

function htmf = plotTFA(TFA, datatype, binArray, chanArray, amprange, twindow, fwindow, blcwin, blctype, fshading, fcontour, Ylog, plotype, surfacetype, cbname, cbscale)


if nargin<16
      cbscale = 'linear'; % 'linear', 'dB', 'whitening'
end

if nargin<15
      cbname = 'jet'; % 'parula' or 'hot'
end
if nargin<14
      surfacetype = '2D'; % '2D' or '3D'
end
if nargin<13
      plotype = 0; % 0 means topo; 1 means rectangular; cell array works for specific rectangular plots
end
if nargin<12
      Ylog = 0;
end
if nargin<11
      fcontour = 'off'; % or  'on'
end
if nargin<10
      fshading = 'flat'; % or  'interp'
end
if nargin<9
      blctype = 'none'; % 'subtractive', 'divisive', 'TSE', or 'none'
end
if nargin<8
      blcwin = []; % ms
end
if nargin<7
      fwindow = [0.5 100]; % range to apply 3-cycle wavelet and getting an actual covered range of 0.49 to ~55 Hz
end
if Ylog
      scalestr = '(log scale)';
else
      scalestr = '';
end

timestart = twindow(1);   %-100;
timeend   = twindow(2);   %600;

if length(twindow)>2
      timeticks = twindow(3:end);
else
      tstepaux  = (timeend-timestart)/5;
      timeticks  = timestart:tstepaux:timeend;
      timeticks  = closest(timestart:timeend*2, timeticks);
end
if isnumeric(amprange)
      if isempty(amprange)
            amprange = 'auto';
      else
            if length(amprange)>2
                  ampticks = amprange(3:end);
            else
                  ampticks = -100:2:100;
                  ampticks = ampticks(ampticks>=amprange(1) & ampticks<=amprange(2));
            end
      end
else
      if ~strcmpi(amprange,'auto')
            error('Invalid string for "amprange". Enter ''auto'' if you want automatic scale for each colorbar')
      end
end
freqstart = fwindow(1);   %1;
freqend   = fwindow(2);   %55;
if length(fwindow)>2
      freqticks = fwindow(3:end);
else
      fstepaux  = (freqend-freqstart)/6;
      freqticks = freqstart:fstepaux:freqend;
      freqticks = closest(0:freqend*2, freqticks);
end
for ibin=1:length(binArray)
      
      switch datatype % 0=power; 1=phase; 2=amplitude; 3=ITC
            case 0
                  Data2plot = TFA.freqdata.Bin(binArray(ibin)).Power;
            case 1
                  Data2plot = TFA.freqdata.Bin(binArray(ibin)).Phase;
            case 2
                  Data2plot = TFA.freqdata.Bin(binArray(ibin)).Ampli;
            case 3
                  Data2plot = TFA.freqdata.Bin(binArray(ibin)).ITC;
            case 4
                  Data2plot = TFA.freqdata.Bin(binArray(ibin)).IndPow;
            otherwise
                  error('Unknown "datatype". It can be 0,1,2,3 or 4 only')
      end
      %if ~strcmpi(blctype, 'none') && ismember(datatype, [0 2]) % power or amplitude
      if ~strcmpi(blctype, 'none') && ismember(datatype, [0 2 3 4]) % power or amplitude or ITC
            %
            %  Baseline correction
            %
            if datatype==0
                  dataword = 'Power';
            elseif datatype==2
                  dataword = 'Amplitude';
            elseif datatype==3
                  dataword = 'ITC';
            elseif datatype==4
                  dataword = 'IndPow';
            else
                  error('LHGVLYFGKUGY')
            end
            fprintf('Baseline correcting the %s (%s) using the window [%.1f  %.1f]...\n', dataword, blctype, blcwin(1), blcwin(2));
            blcmask = TFA.times>blcwin(1) & TFA.times<blcwin(2);
            valuebaseline = mean(Data2plot(:,:,blcmask),3); % to unbaseline later, if needed ...it's cool, isn't it?
            if strcmpi(blctype, 'subtractive')
                  Data2plot = Data2plot - repmat(valuebaseline,[1 1 size(Data2plot,3)]);
            elseif strcmpi(blctype, 'divisive')
                  Data2plot = Data2plot./repmat(valuebaseline,[1 1 size(Data2plot,3)]);
            elseif strcmpi(blctype, 'TSE')
                  tseval = repmat(valuebaseline,[1 1 size(Data2plot,3)]);
                  Data2plot = (Data2plot-tseval)./tseval;
            else
                  warning('No baseline correction was performed...');
            end
            %elseif ~strcmpi(blctype, 'none') && ismember(datatype, [1 3]) % phase or ITC
            %      warning('Baseline correction for Phase/ITC data is not available. Sorry');
      elseif ~strcmpi(blctype, 'none') && ismember(datatype, [1]) % phase or ITC
            warning('Baseline correction for Phase data is not available. Sorry');
      else
            %if ismember(datatype, [0 2]) % power or amplitude
            if ismember(datatype, [0 2 3 4]) % power or amplitude
                  warning('Be aware of you did not set a baseline correction...');
            end
      end
      
      fname     = TFA.setname;
      bdescr    = TFA.freqdata.Bin(binArray(ibin)).bindescr;
      period    = TFA.period;
      times     = TFA.times;
      FreqScale = single(1./period);
      
      if iscell(chanArray)
            nchrow  = max(size(chanArray));
            maxchan = max(cell2mat(cellfun(@length, chanArray,'UniformOutput', false)));
            if nchrow>=3
                  axheight = 0.7*(1/nchrow);
            else
                  axheight = 0.6*(1/nchrow);
            end
            ypaux = linspace(axheight,1-axheight, nchrow);
            ypaux = fliplr(ypaux);
            xp = [];
            yp = [];
            chaux = [];
            for k=1:nchrow
                  pch   = chanArray{k};
                  chaux = [chaux pch];
                  Npch3 = length(pch);
                  axwidth = 0.65*(1/maxchan);
                  xp = [xp linspace(axwidth,1-axwidth,Npch3)];
                  yp = [yp repmat(ypaux(k),1,Npch3)];
            end
            
            xp = repmat(xp,1,ceil(TFA.nchan/length(xp)));
            yp = repmat(yp,1,ceil(TFA.nchan/length(yp)));
            
            xvals = xp(1:TFA.nchan);
            yvals = yp(1:TFA.nchan);
            
            chanArray  = chaux;
            nchan2plot = length(chanArray);
            plotype    = 1;
      else
            nchan2plot = length(chanArray);
            if plotype==0
                  %axwidth  = 0.122; %0.058;
                  %axheight = 0.086; %0.046;
                  
                  axwidth  = 0.117;
                  axheight = 0.07;
                  
                  
                  [xvals, yvals] = getprojectedchanloc(TFA, 1:TFA.nchan);
                  xvals = 0.86*(xvals + 0.584);
                  %yvals = 0.82*(yvals + 0.72);
                  yvals = 0.85*(yvals + 0.6);
            else
                  Npch  = ceil(sqrt(TFA.nchan));
                  Npch2 = ceil(sqrt(nchan2plot));
                  
                  if Npch2>1
                        if Npch2>=3
                              axwidth  = 0.72*(1/Npch2);
                              axheight = 0.7*(1/Npch2);
                        else
                              axwidth  = 0.65*(1/Npch2);
                              axheight = 0.6*(1/Npch2);
                        end
                        xp = linspace(axwidth,1-axwidth,Npch2);
                        xp = repmat(xp,1,ceil(TFA.nchan/length(xp)));
                        yp = linspace(axheight,1-axheight,Npch2);
                        yp = fliplr(yp);
                        yp = repmat(yp',1,Npch2);
                        yp = reshape(yp',1,numel(yp));
                        yp = repmat(yp,1,ceil(TFA.nchan/length(yp)));
                  else
                        axwidth  = 0.8;
                        axheight = 0.8;
                        xp = 0.5;
                        xp = repmat(xp,1,ceil(TFA.nchan/length(xp)));
                        yp = 0.5;
                        yp = repmat(yp,1,ceil(TFA.nchan/length(yp)));
                  end
                  xvals = xp(1:TFA.nchan);
                  yvals = yp(1:TFA.nchan);
            end
      end
      
      % create figure
      htmf(ibin) = figure('Name', sprintf('%s - BIN #%g : %s', fname, binArray(ibin), bdescr));
      %colormap(jet);
      colormap(gcf, cbname)
      set(htmf(ibin),'doublebuffer','on');
      set(htmf(ibin), 'Renderer', 'OpenGL');
      drawnow
      X = times;
      Y = FreqScale;
      [~, indX0]= closest(X,0);
      
      for ich=1:nchan2plot
            if chanArray(ich)<=length(xvals)                  
                  Z = double(permute(Data2plot(chanArray(ich),:,:),[2 3 1]));
                  
                  %
                  % colorbar scale (including a spectral whitener)
                  %
                  switch lower(cbscale)
                        case 'linear'
                              % do nothing
                        case 'db'                              
                              switch datatype % 0=power; 1=phase; 2=amplitude; 3=ITC
                                    case {0,4}
                                          Z = 10*log10(Z);
                                    case 1
                                          % do nothing
                                    case 2
                                          Z = 20*log10(Z);
                                    case 3
                                          % do nothing
                                    otherwise
                                          error('Unknown "datatype". It can be 0,1,2,3 or 4 only')
                              end
                              
                        case 'whitened'
                              for wh=1:length(Y)
                                    Z(wh,:) = Z(wh,:).*Y(wh)/10;
                              end
                        case {'db/whitened','whitened/db'}
                              switch datatype % 0=power; 1=phase; 2=amplitude; 3=ITC
                                    case {0,4}
                                          Z = 10*log10(Z);
                                    case 1
                                          % do nothing
                                    case 2
                                          Z = 20*log10(Z);
                                    case 3
                                          % do nothing
                                    otherwise
                                          error('Unknown "datatype". It can be 0,1,2,3 or 4 only')
                              end
                              for wh=1:length(Y)
                                    Z(wh,:) = Z(wh,:).*Y(wh)/10;
                              end
                        otherwise
                              % do nothing
                  end
                  
                  maxZ = max(Z(:));
                                  
                  if strcmpi(TFA.chanlocs(chanArray(ich)).labels, 'EVEOGL') && plotype==0
                        axes('Units','Normal','Position',[0.90 0.05 axwidth*1.5 axheight*1.5]);
                        
                        if strcmpi(surfacetype,'3D')
                              htf = surf(X,Y,Z); % option 2: 3-D shaded surface plot                              
                        else
                              htf = pcolor(X,Y,Z); % standard 2-D plot (use shading('interp') with this)                              
                        end
                        
                        shading(fshading)
                        
                        if ischar(fcontour)
                              if strcmpi(fcontour,'on')
                                    hold on
                                    contourf(X, Y, Z, 30); % filled 2-D contou
                                    hold off
                              end
                        elseif isnumeric(fcontour)
                              hold on
                              contourf(X, Y, Z, fcontour); % filled 2-D contour
                              hold off
                        end                        
                        if strcmpi(surfacetype,'3D')                              
                              %
                              % X0 line
                              %
                              hold on
                              plot3([0 0],[0 freqend],[maxZ maxZ],'--k','LineWidth', 1);
                              hold off
                        else                              
                              %
                              % X0 line
                              %
                              hold on
                              plot([0 0],[0 freqend],'--k','LineWidth', 1);
                              hold off
                        end
                  else
                        if plotype==0
                              axes('Units','Normal','Position',[xvals(chanArray(ich))-axwidth/2 yvals(chanArray(ich))-axheight/2 axwidth axheight]);
                        else
                              axes('Units','Normal','Position',[xvals(ich)-axwidth/2 yvals(ich)-axheight/2 axwidth axheight]);
                        end                        
                        if strcmpi(surfacetype,'3D')
                              htf = surf(X,Y,Z); % option 2: 3-D shaded surface plot                              
                        else
                              htf = pcolor(X,Y,Z); % standard 2-D plot (use shading('interp') with this)                              
                        end
                        
                        shading(fshading)
                        %camlight right
                        %lighting phong
                        
                        if ischar(fcontour)
                              if strcmpi(fcontour,'on')
                                    hold on
                                    contourf(X, Y, Z, 30); % filled 2-D contour
                                    hold off
                              end
                        elseif isnumeric(fcontour)
                              hold on
                              contourf(X, Y, Z, fcontour); % filled 2-D contour
                              hold off
                        end                        
                        if strcmpi(surfacetype,'3D')
                              %
                              % X0 line
                              %
                              hold on
                              plot3([0 0],[freqstart freqend],[maxZ maxZ],'--k','LineWidth', 1);
                              plot3([0 0],[freqstart freqstart],[0 maxZ],'--k','LineWidth', 1);
                              plot3([0 0],[freqend freqend],[0 maxZ],'--k','LineWidth', 1);
                              hold off
                        else
                              %
                              % X0 line
                              %
                              hold on
                              plot([0 0],[0 freqend],'--k','LineWidth', 1);
                              hold off
                        end
                  end
                  
                  %title([num2str(chanArray(ich)) ' (' TFA.chanlocs(chanArray(ich)).labels ') : '  bdescr]);
                  title([num2str(chanArray(ich)) ' (' TFA.chanlocs(chanArray(ich)).labels ')']);
                  
                  if Ylog
                        set(gca,'YScale','log')
                  end
                  
                  set(gca,'YTick',freqticks)                  
                  axis([timestart timeend freqstart freqend])
                  if ischar(amprange)
                        %amprange = [min(Z(:)) max(Z(:))]
                        caxis auto
                  else
                        caxis(gca, amprange)
                  end
                  
                  set(gca,'XTick', timeticks)
                  set(htf,'DisplayName', bdescr);
                  set(gca,'XMinorTick','on','YMinorTick','on')
                  drawnow                  
            else
                  fprintf('ch#%g : no channel location...\n', chanArray(ich));
            end
      end
       
      ylabelstr = sprintf('ylabel(''''Frequency (Hz) %s''''); ', scalestr);
      YticksLabelStr = sprintf('set(gca, ''''%s'''', [%s]); ', 'YTick', vect2colon(freqticks, 'Delimiter', 'off') );
      XticksLabelStr = sprintf('set(gca, ''''%s'''', [%s]); ', 'XTick', vect2colon(timeticks, 'Delimiter', 'off') );
      colorbarLabel  = sprintf('ylabel(hcolb, ''''%s''''); ', cbscale);
      figcmmd1    = 'txttl = get(gca, ''''title''''); ';
      figcmmd2    = 'txttl2 = txttl.Text.String; ';
      figuretitle = sprintf('[txttl2 '''':%s'''']', bdescr);
      figuretitle = sprintf('set(gcf, ''''%s'''', %s); ', 'name',  figuretitle);      
      com = ['axis on; ' ...
             'clear xlabel ylabel; '...
             'hcolb = colorbar; '...
             colorbarLabel...
             'legend(''''off''''); ' ...
             'xlabel(''''Time (ms)''''); ' ...            
             ylabelstr...
             YticksLabelStr...
             XticksLabelStr...
             figcmmd1...
             figcmmd2...
             figuretitle];
      
      axcopy(htmf(ibin), com); % turn on popup feature
end
if ischar(amprange)
warning('Be aware that you are using automatic scaling. This means that channel may have different colorbar scales');
end




