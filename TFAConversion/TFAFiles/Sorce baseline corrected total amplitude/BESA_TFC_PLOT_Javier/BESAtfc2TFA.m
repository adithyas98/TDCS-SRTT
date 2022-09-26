% BESAtfc2TFA converts a *.tfc file into a *.tfa (Javier's format) file
%
% Use as
%   TFA = BESAtfc2TFA(filename, fs)
%
% % The output is a structure containing the following fields:
% 'setname'             :
% 'filename'            :
% 'filepath'            :
% 'workfiles'           :
% 'subject'             :
% 'nchan'               : number of channels
% 'nbin'                : number of bins (conditiona). Only 1 allowed at
%                         the current version....Sorry
% 'omega'               :
% 'minfreq'             : lowest frequency
% 'maxfreq'             : highest frequency
% 'period'              : 1/frequencies
% 'freq'                : frequency array
% 'srate'               : sample rate
% 'xmin'                : lowest time
% 'xmax'                : highest time
% 'times'               : time array
% 'freqdata'            : DATA! 
% 'datatype'            : type of data to estimate 0=POWER; 1=PHASE; 2=AMPLITUDE; 3=ITC; 4=Induced Power
% 'baseline'            :
% 'chanlocs'            :
% 'ref'                 :
% 'bindescr'            : name of analyzed condition
% 'ntrials'             : number of trials on which the data is based
% 'pexcluded'           :
% 'history'             :
% 'saved'               :
% 'version'             :
% 'FinalSelectedEpochs' :
%
% Author: Javier Lopez-Calderon
% February 27th, 2019
% Talca, Chile

function TFA = BESAtfc2TFA(filename, fs)

tfc = readBESAtfc(filename);

sname = strrep(filename,'.tfc','');

TFA = struct(...
'setname',  {sname},...
'filename', {[sname '.tfa']},...
'filepath', {''},...
'workfiles',{''},...
'subject',  {''},...
'nchan',    {size(tfc.Data,1)},...
'nbin',     {1},...
'omega',    {3},...
'minfreq',  {min(tfc.Frequency)},...
'maxfreq',  {max(tfc.Frequency)},...
'period',   {1./tfc.Frequency},...
'freq',     {tfc.Frequency},...
'srate',    {fs},...
'xmin',     {min(tfc.Time)/1000},...
'xmax',     {max(tfc.Time)/1000},...
'times',    {tfc.Time },...
'freqdata', {struct('Bin',struct('Power',[],'Phase',[],'bindescr',''))},...
'datatype', {'TFA'},...
'baseline', {[]},...
'chanlocs', {struct([])},...
'ref',      {'common'},...
'bindescr', {tfc.ConditionName},...
'ntrials',  {[]},...
'pexcluded',{0},...
'history',  {''},...
'saved',    {'no'},...
'version',  {'4.0.6.0'},...
'FinalSelectedEpochs',{[]});

Datax = permute(tfc.Data,[1 3 2]);
for k=1:length(tfc.Time)
    TFA.freqdata.Bin.Power(:,:,k)= double(Datax(:,:,k));
end
TFA.freqdata.Bin.Phase    = [];
TFA.freqdata.Bin.bindescr = tfc.ConditionName;
ChannelLabels = strrep(cellstr(tfc.ChannelLabels),'''','')';

for k=1:length(ChannelLabels)
    TFA.chanlocs(k).labels = ChannelLabels{k};
end