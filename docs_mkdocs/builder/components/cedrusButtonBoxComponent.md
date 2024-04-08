# cedrusButtonBoxComponent
An event class for checking an Cedrus RBxxx button boxes
    using XID library

    This is based on keyboard component, several important differences:
    - no special response class analogous to event.BuilderKeyResponse()
    - enabled responses (active keys) are handled by the hardware device

    More than one component in a routine will produce conflicts between
    components over which active keys (for responses and lights).


> **Categories:** Responses
> **Works in:** PsychoPy

## Parameters

### Basic

#### `Name`
> Name of this Component (alphanumeric or _, no spaces)

#### `Start type`
> How do you want to define your start point?
> 
> Options:
> - time (s)
> - frame N
> - condition

#### `Stop type`
> How do you want to define your end point?
> 
> Options:
> - duration (s)
> - duration (frames)
> - time (s)
> - frame N
> - condition

#### `Start`
> When does the Component start?

#### `Stop`
> When does the Component end? (blank is endless)

#### `Expected start (s)`
> (Optional) expected start (s), purely for representing in the timeline

#### `Expected duration (s)`
> (Optional) expected duration (s), purely for representing in the timeline

#### `Register keypress on...`
> When should the keypress be registered? As soon as pressed, or when released?
> 
> Options:
> - press
> - release

#### `Allowed keys`
> Keys to be read (blank for any) or key numbers separated by commas

#### `Force end of Routine`
> Should a response force the end of the Routine (e.g end the trial)?

### Data

#### `Save onset/offset times`
> Store the onset/offset times in the data file (as well as in the log file).

#### `Sync timing with screen`
> A reaction time to a visual stimulus should be based on when the screen flipped

#### `Discard previous`
> Do you want to discard all responses occurring before the onset of this Component?

#### `Store`
> Choose which (if any) responses to store at the end of a trial
> 
> Options:
> - last key
> - first key
> - all keys
> - nothing

#### `Store correct`
> Do you want to save the response as correct/incorrect?

#### `Correct answer`
> What is the 'correct' response? NB, buttons are labelled 0 to 6 on a 7-button box. Enter 'None' (no quotes) if withholding a response is correct. Might be helpful to add a correctAns column and use $correctAns to compare to the key press.

### Testing

#### `Disable Component`
> Disable this Component

### Device

#### `Device label`
> A label to refer to this Component's associated hardware device by. If using the same device for multiple components, be sure to use the same label here.

### Hardware

#### `deviceNumber`
> Device number, if you have multiple devices which one do you want (0, 1, 2...)

#### `useBoxTimer`
> According to Cedrus the response box timer has a drift - use with caution!
> 
> Options:
> - True
> - False

